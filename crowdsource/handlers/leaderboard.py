import tornado.gen
import ujson
from tornado.concurrent import run_on_executor

from ..enums import CompetitionType
from ..persistence.models import Submission
from .base import AuthenticatedHandler
from .validate import validate_leaderboard_get


class LeaderboardHandler(AuthenticatedHandler):
    @tornado.gen.coroutine
    def get(self):
        """Get the current list of competition ids"""
        yield self._get()

    @run_on_executor
    def _get(self):
        data = self._validate(validate_leaderboard_get)

        res = []
        with self.session() as session:
            submissions = session.query(Submission).all()
            for x in submissions:
                for c in x:
                    submission_id = data.get("submission_id", ())
                    cpid = data.get("competition_id", ())
                    clid = data.get("user_id", ())
                    user_username = data.get("user_username", ())
                    t = data.get("type", "")

                    if submission_id and c.submission_id not in submission_id:
                        continue
                    if cpid and c.competition_id not in cpid:
                        continue
                    if clid and c.user_id not in clid:
                        continue
                    if t and CompetitionType(t) != c.competition.spec.type:
                        continue
                    if user_username and c.user.username != user_username:
                        continue

                    d = c.to_dict(private=True)
                    d["score"] = round(d["score"], 2)
                    res.append(d)

            page = int(data.get("page", 0))
            self.write(
                ujson.dumps(res[page * 100 : (page + 1) * 100])
            )  # return top 100
