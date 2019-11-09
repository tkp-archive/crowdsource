import ujson
from .base import ServerHandler
from ..utils import _CLIENT_NOT_REGISTERED, _REGISTER
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
        user = self.get_argument('id', '')
        if not user and self.current_user:
            user = self.current_user.decode('utf-8')
        with self.session() as session:
            client = session.query(Client).filter_by(id=int(user)).first()
            if client:
                ret = self._login_post(client)
                self._writeout(ujson.dumps(ret), _REGISTER, ret["id"])
            else:
                import ipdb; ipdb.set_trace()
                self._set_401(_CLIENT_NOT_REGISTERED)


class LogoutHandler(ServerHandler):
    def get(self):
        '''Get the logout page'''
        self.clear_cookie("user")
