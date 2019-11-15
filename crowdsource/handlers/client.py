import tornado.gen
import tornado.escape
import tornado.web
import ujson
from tornado.concurrent import run_on_executor
from .base import ServerHandler
from ..persistence.models import Client, APIKey


class RegisterHandler(ServerHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        '''Get the current list of client ids'''
        yield self._get()

    @run_on_executor
    def _get(self):
        if self.current_user and int(self.current_user) not in self._clients:
            return self.post()

        # paginate
        page = int(self.get_argument('page', 0))
        self.write(ujson.dumps([c.to_dict() for c in list(self._clients.values())[page * 100:(page + 1) * 100]]))

    @tornado.gen.coroutine
    def post(self):
        '''Register a client. Client will be assigned a session id'''
        yield self._post()

    @run_on_executor
    def _post(self):
        try:
            body = tornado.escape.json_decode(self.request.body or '{}')
        except ValueError:
            body = {}
        username = self.get_argument('username', body.get('username', ''))
        email = self.get_argument('email', body.get('email', ''))
        password = self.get_argument('password', body.get('password', ''))

        if not username or not email or not password:
            self._set_400("Client malformed")

        with self.session() as session:
            c = Client(username=username, email=email, password=password)

            try:
                session.add(c)
                session.commit()
                session.refresh(c)
                ret = self._login_post(c)
                self._writeout(ujson.dumps(ret), "Registering client {}", ret["client_id"])
                return
            except BaseException:
                self._set_400("Client malformed")
                return


class APIKeyHandler(ServerHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        yield self._get()

    @run_on_executor
    def _get(self):
        with self.session() as session:
            client = session.query(Client).filter_by(client_id=int(self.current_user)).first()
            if not client:
                self._set_400("Client malformed")
            self.write({a.apikey_id: a.to_dict() for a in client.apikeys})

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        yield self._post()

    @run_on_executor
    def _post(self):
        with self.session() as session:
            client = session.query(Client).filter_by(client_id=int(self.current_user)).first()
            if not client:
                self._set_400("Client malformed")
            if self.get_argument("id", ""):
                # delete key
                key = session.query(APIKey).filter_by(apikey_id=int(self.get_argument("id"))).first()
                if key.client == client:
                    session.delete(key)
                else:
                    self._set_401("Unauthorized to delete key")
            else:
                # new key
                apikey = APIKey(client=client)
                session.add(apikey)
