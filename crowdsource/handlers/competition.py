import tornado.web
import ujson
from datetime import datetime
from .base import ServerHandler
from .validate import validate_competition_get, validate_competition_post
from ..types.competition import CompetitionSpec
from ..persistence.models import Competition


class CompetitionHandler(ServerHandler):
    def get(self, *args, **kwargs):
        '''Get the current list of competition ids'''
        data = self._validate(validate_competition_get)
        res = []
        with self.session() as session:
            competitions = session.query(Competition).all()
            for c in competitions:
                competition_id = data.get('competition_id', ())
                clid = data.get('client_id', ())
                t = data.get('type', ())

                if competition_id and c.competition_id not in competition_id:
                    continue

                if clid and c.client_id not in clid:
                    continue

                if t and c.spec.type not in t:
                    continue

                # check if expired and turn off if necessary
                if datetime.now() > c.expiration:
                    c.active = False

                    if self.get_argument('current', False):
                        continue

                res.append(c.to_dict())

        page = int(data.get('page', 0))
        self.write(ujson.dumps(res[page * 100:(page + 1) * 100]))  # return top 100

    @tornado.web.authenticated
    def post(self):
        '''Register a competition. Competition will be assigned a session id'''
        data = self._validate(validate_competition_post)

        # generate a new ID
        with self.session() as session:
            client_id = int(self.current_user)
            try:
                spec = CompetitionSpec.from_dict(data["spec"])
                comp = Competition.from_spec(client_id=client_id, spec=spec)
            except (KeyError, ValueError):
                self._set_400("Competition malformed")
                return

            session.add(comp)
            session.commit()
            session.refresh(comp)

            if comp.competition_id:
                # put in perspective
                self._competitions.update([comp.to_dict()])
                self._writeout(ujson.dumps({'competition_id': str(comp.competition_id)}), "Registering competitiong %s for client %s", comp.competition_id, comp.client_id)
            else:
                self._set_400("Competition malformed")
