import logging
import six
import tornado.web
import ujson
from datetime import datetime
from .base import ServerHandler
from .validate import validate_submission_get, validate_submission_post
from ..persistence.models import Submission, Competition
from ..types.submission import SubmissionSpec
from ..types.utils import fetchDataset, checkAnswer
from ..utils import _REGISTER_SUBMISSION, _SUBMISSION_MALFORMED, _COMPETITION_NOT_REGISTERED
from ..enums import CompetitionType


class SubmissionHandler(ServerHandler):
    @tornado.web.authenticated
    def get(self):  # TODO make coroutine
        '''Get the current list of competition ids'''
        data = self._validate(validate_submission_get)

        # first, grade any pending submissions that are now available
        self.score_laters()

        res = []
        with self.session() as session:
            submissions = session.query(Submission).all()
        for x in submissions:
            for c in x:
                id = data.get('id', ())
                cpid = data.get('competition_id', ())
                clid = data.get('client_id', ())
                t = data.get('type', '')

                if id and c.id not in id:
                    continue
                if cpid and c.competitionId not in cpid:
                    continue
                if clid and c.clientId not in clid:
                    continue
                if t and CompetitionType(t) != c.competition.spec.type:
                    continue

                # only allow if im the submitter or the competition owner
                if (self.current_user != c.clientId) and (self.current_user != c.competition.clientId):
                    continue

                # check if expired and turn off if necessary
                if datetime.now() > c.competition.expiration:
                    c.competition.active = False

                d = c.to_dict(private=True)
                d['score'] = round(d['score'], 2)
                res.append(d)

        page = int(data.get('page', 0))
        self.write(ujson.dumps(res[page*100:(page+1)*100]))  # return top 100

    @tornado.web.authenticated
    def post(self):
        '''Register a competition. Competition will be assigned a session id'''
        data = self._validate(validate_submission_post)

        submission = data['submission']
        client_id = data['id']
        competitionId = data['competition_id']

        with self.session() as session:
            competition = session.query(Competition).filter_by(id=int(competitionId)).first()
            if not competition:
                self._set_400(_COMPETITION_NOT_REGISTERED)
                return

            if datetime.now() > competition.expiration:
                competition.active = False
                self.write('{}')
                return

            try:
                spec = SubmissionSpec.from_dict(submission)
                submission = Submission.from_spec(client_id=client_id,
                                                  competitionId=competitionId,
                                                  competition=competition,
                                                  spec=spec,
                                                  score=-1.0)
            except (KeyError, ValueError, AttributeError):
                self._set_400(_SUBMISSION_MALFORMED)

            # persist
            with self.session() as session:
                session.add(submission)
                session.commit()
                session.refresh(submission)

            if not submission.id:
                self._set_400(_SUBMISSION_MALFORMED)

            # put in perspective
            self._submissions.update([submission.to_dict()])

            id = submission.id
            competitionId = submission.competitionId

            # calculate result if immediate
            if competition.answer_delay <= 0:
                score = self.score(submission)

            else:
                self.score_later(submission)
                score = {'id': id}

        self._writeout(ujson.dumps(score), _REGISTER_SUBMISSION, id, submission.clientId)

    def score(self, submission):
        logging.info("SCORING %s FOR %s", str(submission.id), submission.competitionId)
        score = checkAnswer(submission)
        submission.score = score
        with self.session() as session:
            submission.score = score
            session.commit()
        return submission.to_json()

    def score_later(self, submission):
        logging.info("Stashing submission %s for competition %s to score later", submission.id, submission.competitionId)
        self._to_score_later.append(submission)

    def score_laters(self):
        to_score_now = [s for s in self._to_score_later if datetime.now() > s.competition.expiration]
        logging.info('Scoring %s submissions now', len(to_score_now))

        ret = []

        for s in to_score_now:
            competition = s.competition
            df = fetchDataset(competition)

            # FIXME
            if isinstance(competition.targets, dict):
                df = df[df[competition.dataset_key].isin(list(set(competition.current_state[competition.dataset_key].values)))][competition.current_state.columns]
            elif isinstance(competition.targets, list):
                df = df[competition.spec.targets][competition.current_state.columns]
            elif isinstance(competition.targets, six.string_types):
                df = df[[competition.spec.targets]][competition.current_state.columns]

            cur = len(competition.current_state.index)
            if len(df.index) > cur:
                competition.answer = df[df.index == df.index[-1]]
                ret.append(self.score(s))

                with self.session() as session:
                    s.score = s.score
                    session.commit()
                self._to_score_later.remove(s)

            else:
                logging.info('SKIPPING %d', s.id)

        logging.info('%s left to score', len(self._to_score_later))
        return ret
