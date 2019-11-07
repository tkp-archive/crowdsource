import ujson
from .base import ServerHandler
from ..utils import _CLIENT_NOT_REGISTERED, _REGISTER
from ..structs import ClientStruct


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

        ret = self._login_post(ClientStruct(id=user))
        if ret:
            self._writeout(ujson.dumps(ret), _REGISTER, ret["id"])
        else:
            self._set_401(_CLIENT_NOT_REGISTERED)


class LogoutHandler(ServerHandler):
    def get(self):
        '''Get the logout page'''
        self.clear_cookie("user")
