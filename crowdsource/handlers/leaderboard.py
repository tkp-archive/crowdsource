import tornado.gen
import ujson
from tornado.concurrent import run_on_executor
from .base import ServerHandler
from .validate import validate_leaderboard_get
from ..persistence.models import Submission
from ..enums import CompetitionType


class LeaderboardHandler(ServerHandler):
    @tornado.gen.coroutine
    def get(self):
        '''Get the current list of competition ids'''
        yield self._get()

    @run_on_executor
    def _get(self):
        data = self._validate(validate_leaderboard_get)

        res = []
        with self.session() as session:
            submissions = session.query(Submission).all()
            for x in submissions:
                for c in x:
                    submission_id = data.get('submission_id', ())
                    cpid = data.get('competition_id', ())
                    clid = data.get('client_id', ())
                    t = data.get('type', '')
                    if submission_id and c.submission_id not in submission_id:
                        continue
                    if cpid and c.competition_id not in cpid:
                        continue
                    if clid and c.client_id not in clid:
                        continue
                    if t and CompetitionType(t) != c.competition.spec.type:
                        continue

                    d = c.to_dict(private=True)
                    d['score'] = round(d['score'], 2)
                    res.append(d)

            page = int(data.get('page', 0))
            self.write(ujson.dumps(res[page * 100:(page + 1) * 100]))  # return top 100
