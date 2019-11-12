import tornado.escape
import ujson
from .base import ServerHandler
from ..persistence.models import Client


class LoginHandler(ServerHandler):
    def get(self):
        '''Get the login page'''
        if self.current_user:
            self.redirect('api/v1/register')
        else:
            self.redirect('login')

    def post(self):
        '''Login'''
        body = tornado.escape.json_decode(self.request.body or '{}')
        username = self.get_argument('username', body.get('username', ''))
        password = self.get_argument('password', body.get('password', ''))

        if not username or not password:
            if self.current_user:
                client_id = self.current_user.decode('utf-8')
                with self.session() as session:
                    client = session.query(Client).filter_by(client_id=client_id).first()
                    if client:
                        self.login(client)
                        return

            self._set_400("Client malformed")

        with self.session() as session:
            client = session.query(Client).filter_by(username=username).first()
            if client and (client or not password) and (client.password == password):
                self.login(client)
            else:
                self._set_400("Client not registered")

    def login(self, client):
        ret = self._login_post(client)
        self._writeout(ujson.dumps(ret), "Registering client %s", ret["client_id"])


class LogoutHandler(ServerHandler):
    def get(self):
        '''clear cookie'''
        self.clear_cookie("user")

    def post(self):
        '''Get the logout page'''
        self.clear_cookie("user")
