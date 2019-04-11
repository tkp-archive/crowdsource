import tornado.web
import os.path
import crowdsource
from crowdsource.login import null_login
from crowdsource.persistence import null_persist
from crowdsource.registration import null_register
from crowdsource.handlers import LoginHandler
from mock import MagicMock


class TestLogin:
    def setup(self):
        settings = {
                "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                "login_url": "/login",
                "debug": "True",
                "template_path": os.path.join(os.path.dirname(crowdsource.__file__), 'assets'),
                }
        self.app = tornado.web.Application(**settings)
        self.app._transforms = []

    def test_LoginHandler(self):
        req = MagicMock()
        req.body = ''
        context = {'clients': {1234: ''},
                   'competitions': {},
                   'leaderboards': {},
                   'submissions': {},
                   'stash': [],
                   'login': null_login,
                   'register': null_register,
                   'persist': null_persist}
        x = LoginHandler(self.app, req, **context)
        x._transforms = []
        x._validate = lambda *args: True
        x.current_user = True
        x.get()

        x = LoginHandler(self.app, req, **context)
        x._transforms = []
        x._validate = lambda *args: True
        x.current_user = False
        x.get()
