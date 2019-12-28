import copy
from crowdsource.handlers.base import ServerHandler
from mock import MagicMock
from tornado.web import HTTPError

CONTEXT = {'clients': {},
           'competitions': {},
           'leaderboards': {},
           'submissions': {},
           'stash': [],
           'all_clients': MagicMock(),
           'all_competitions': MagicMock(),
           'all_submissions': MagicMock(),
           'sessionmaker': MagicMock()}


class TestBase:
    def setup(self):
        self.app = MagicMock()
        self.app._transforms = []

    def test_get_current_user(self):
        req = MagicMock()
        req.body = ''
        context = copy.deepcopy(CONTEXT)

        x = ServerHandler(self.app, req, **context)
        x._transforms = []
        x.get_secure_cookie = MagicMock(return_value=b'5')
        assert x.get_current_user() == '5'

    def test_set_401(self):
        req = MagicMock()
        req.body = ''
        context = copy.deepcopy(CONTEXT)

        x = ServerHandler(self.app, req, **context)
        x._transforms = []
        try:
            x._set_401('test')
            assert False
        except HTTPError:
            pass

    def test_set_403(self):
        req = MagicMock()
        req.body = ''
        context = copy.deepcopy(CONTEXT)

        x = ServerHandler(self.app, req, **context)
        x._transforms = []
        try:
            x._set_403('test')
            assert False
        except HTTPError:
            pass

    def test_validate(self):
        req = MagicMock()
        req.body = ''
        context = copy.deepcopy(CONTEXT)

        x = ServerHandler(self.app, req, **context)
        x._transforms = []
        x._validate(None)

    def test_writeout(self):
        req = MagicMock()
        req.body = ''
        context = copy.deepcopy(CONTEXT)

        x = ServerHandler(self.app, req, **context)
        x._transforms = []
        x._writeout('test', 'test')
