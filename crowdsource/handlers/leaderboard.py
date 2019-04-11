import tornado.web
import ujson
from .base import ServerHandler
from ..utils.enums import CompetitionType
from ..utils.validate import validate_leaderboard_get


class LeaderboardHandler(ServerHandler):
    @tornado.web.authenticated
    def get(self):  # TODO make coroutine
        '''Get the current list of competition ids'''
        self._authenticate()

        data = self._validate(validate_leaderboard_get)

        res = []
        for x in self._submissions.values():
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

                d = c.to_dict(private=True)
                d['score'] = round(d['score'], 2)
                res.append(d)

        page = int(data.get('page', 0))
        self.write(ujson.dumps(res[page*100:(page+1)*100]))  # return top 100
