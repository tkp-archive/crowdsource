import tornado.web
import ujson
from datetime import datetime
from .base import ServerHandler
from .validate import validate_competition_get, validate_competition_post
from ..persistence.models import Competition
from ..structs import CompetitionStruct
from ..utils import _REGISTER_COMPETITION, _COMPETITION_MALFORMED


class CompetitionHandler(ServerHandler):
    def get(self, *args, **kwargs):
        '''Get the current list of competition ids'''
        data = self._validate(validate_competition_get)
        res = []
        with self.session() as session:
            competitions = session.query(Competition).all()
            for c in competitions:
                id = data.get('id', ())
                clid = data.get('client_id', ())
                t = data.get('type', ())

                if id and c.id not in id:
                    continue

                if clid and c.clientId not in clid:
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
        self.write(ujson.dumps(res[page*100:(page+1)*100]))  # return top 100

    @tornado.web.authenticated
    def post(self):
        '''Register a competition. Competition will be assigned a session id'''
        data = self._validate(validate_competition_post)

        # generate a new ID
        client_id = data['id']
        try:
            comp = CompetitionStruct(id=-1, clientId=client_id, spec=data['spec'])
        except (KeyError, ValueError):
            self._set_400(_COMPETITION_MALFORMED)

        with self.session() as session:
            competitionSql = comp.to_sql()
            session.add(competitionSql)
            session.commit()
            session.refresh(competitionSql)

            # put in perspective
            self._competitions.update([competitionSql.to_dict()])

        if comp.id:
            self._competitions.update(comp.to_dict())
            self._writeout(ujson.dumps({'id': str(comp.id)}), _REGISTER_COMPETITION, comp.id, comp.clientId)
        else:
            self._set_400(_COMPETITION_MALFORMED)
