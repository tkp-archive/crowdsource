import tornado.gen
import tornado.web
import ujson
from datetime import datetime
from tornado.concurrent import run_on_executor
from .base import AuthenticatedHandler
from .validate import validate_competition_get, validate_competition_post
from ..types.competition import CompetitionSpec
from ..persistence.models import Competition


class CompetitionHandler(AuthenticatedHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self._get()

    @run_on_executor
    def _get(self, *args, **kwargs):
        """Get the current list of competition ids"""
        data = self._validate(validate_competition_get)
        res = []
        with self.session() as session:
            competitions = session.query(Competition).all()
            for c in competitions:
                competition_id = data.get("competition_id", ())
                clid = data.get("user_id", ())
                user_username = data.get("user_username", ())
                t = data.get("type", ())

                if competition_id and c.competition_id not in competition_id:
                    continue
                if clid and c.user_id not in clid:
                    continue
                if t and c.spec.type not in t:
                    continue
                if user_username and c.user.username != user_username:
                    continue

                # check if expired and turn off if necessary
                if datetime.now() > c.expiration:
                    c.active = False

                    if self.get_argument("current", False):
                        continue
                res.append(c.to_dict())

        self.write(ujson.dumps(res))

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        """Register a competition. Competition will be assigned a session id"""
        yield self._post()

    @run_on_executor
    def _post(self):
        data = self._validate(validate_competition_post)

        # generate a new ID
        with self.session() as session:
            user_id = int(self.current_user)
            try:
                spec = CompetitionSpec.from_dict(data["spec"])
                comp = Competition.from_spec(user_id=user_id, spec=spec)
            except (KeyError, ValueError):
                self._set_400("Competition malformed")
                return

            session.add(comp)
            session.commit()
            session.refresh(comp)

            if comp.competition_id:
                # put in perspective
                self._competitions.update([comp.to_dict()])
                self._all_competitions.update([comp.to_dict()])
                self._writeout(
                    ujson.dumps({"competition_id": str(comp.competition_id)}),
                    "Registering competitiong %s for user %s",
                    comp.competition_id,
                    comp.user_id,
                )
            else:
                self._set_400("Competition malformed")
