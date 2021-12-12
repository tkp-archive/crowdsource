import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from .base import AuthenticatedHandler


class AdminHandler(AuthenticatedHandler):
    @tornado.gen.coroutine
    def get(self):
        """Get the current list of user ids"""
        yield self._get()

    @run_on_executor
    def _get(self):
        if self.current_user and self.is_admin():
            self.write("")
            return
        self._set_401("Not admin")
