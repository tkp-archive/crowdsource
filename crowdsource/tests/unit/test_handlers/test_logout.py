import tornado.web
import os.path
import crowdsource
from crowdsource.handlers import LogoutHandler
from mock import MagicMock


class TestLogout:
    def setup(self):
        settings = {
                "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                "login_url": "/login",
                "debug": "True",
                "template_path": os.path.join(os.path.dirname(crowdsource.__file__), 'assets'),
                }
        self.app = tornado.web.Application(**settings)
        self.app._transforms = []

    def test_LogoutHandler(self):
        req = MagicMock()
        req.body = ''
        context = {'clients': {1234: ''},
                   'competitions': {},
                   'leaderboards': {},
                   'submissions': {},
                   'stash': [],
                   'all_clients': MagicMock(),
                   'all_competitions': MagicMock(),
                   'all_submissions': MagicMock(),
                   'sessionmaker': MagicMock()}

        x = LogoutHandler(self.app, req, **context)
        x._transforms = []
        x._validate = lambda *args: True
        x.current_user = True
        x.get()
