import tornado.web
from .base import ServerHandler


class AdminHandler(ServerHandler):
    @tornado.web.authenticated
    def get(self):
        '''Get the current list of client ids'''
        if self.is_admin():
            self._writeout("", "Admin")
            return
        self._set_401("Not admin")
