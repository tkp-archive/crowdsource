import tornado.gen
from tornado.concurrent import run_on_executor
from .base import ServerHandler
from ..persistence.models import Client
from ..utils import parse_body


class LoginHandler(ServerHandler):
    @tornado.gen.coroutine
    def get(self):
        '''Get the login page'''
        yield self._get()

    @run_on_executor
    def _get(self):
        if self.current_user:
            self.redirect('api/v1/register')
        else:
            self.redirect(self.basepath + "home")

    @tornado.gen.coroutine
    def post(self):
        '''Login'''
        if self.current_user:
            client_id = self.current_user
            with self.session() as session:
                client = session.query(Client).filter_by(client_id=client_id).first()
                if client:
                    self.login(client)
                    return
        body = parse_body(self.request)
        username = self.get_argument('username', body.get('username', ''))
        password = self.get_argument('password', body.get('password', ''))

        if not username or not password:
            client_id = self.get_user_from_key()
            if not client_id:
                self._set_400("Client not registered")
            return

        if not self.get_user_from_username_password():
            self._set_400("Client not registered")


class LogoutHandler(ServerHandler):
    def get(self):
        '''clear cookie'''
        self.clear_cookie("user")
        self.redirect(self.basepath + "home")

    def post(self):
        '''Get the logout page'''
        self.clear_cookie("user")
