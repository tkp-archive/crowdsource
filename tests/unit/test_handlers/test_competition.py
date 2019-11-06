import tornado.web
from crowdsource.handlers import CompetitionHandler
from crowdsource.utils.enums import CompetitionType
from datetime import datetime
from mock import MagicMock
from tornado.web import HTTPError


class TestCompetitions:
    def setup(self):
        self.app = tornado.web.Application(cookie_secret='test')
        self.app._transforms = []

    def test_CompetitionHandler(self):
        req = MagicMock()
        req.body = ''
        context = {'clients': {1234: ''},
                   'competitions': {},
                   'leaderboards': {},
                   'submissions': {},
                   'stash': [],
                   'sessionmaker': MagicMock()}

        x = CompetitionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True

        # requires client id
        x.get()
        try:
            x.post()
            assert False
        except HTTPError:
            pass

        assert(x.get_status() == 401)

        # malformed competition
        req.body = '{"id":1234}'
        x = CompetitionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True
        try:
            x.post()
            assert False
        except HTTPError:
            pass

        assert(x.get_status() == 400)

    def test_competitions2(self):
        req = MagicMock()
        req.body = ''
        x = {0: MagicMock(), 1: MagicMock(), 2: MagicMock(), 3: MagicMock(), 4: MagicMock(), 5: MagicMock()}
        x[0].id = 0
        x[1].id = 1
        x[2].id = 1
        x[3].id = 2
        x[4].id = 2
        x[5].id = 2

        x[0].clientId = 0
        x[1].clientId = 0
        x[2].clientId = 1
        x[3].clientId = 2
        x[4].clientId = 2
        x[5].clientId = 2

        x[0].spec.type = CompetitionType.PREDICT
        x[1].spec.type = CompetitionType.PREDICT
        x[2].spec.type = CompetitionType.PREDICT
        x[3].spec.type = CompetitionType.CLASSIFY
        x[4].spec.type = CompetitionType.CLASSIFY
        x[5].spec.type = CompetitionType.CLASSIFY

        x[0].expiration = datetime(2019, 1, 1)
        x[1].expiration = datetime(2019, 1, 1)
        x[2].expiration = datetime(2019, 1, 1)
        x[3].expiration = datetime(2019, 1, 1)
        x[4].expiration = datetime(2017, 1, 1)
        x[5].expiration = datetime(2019, 1, 1)

        context = {'clients': {1234: ''},
                   'competitions': x,
                   'leaderboards': {},
                   'submissions': {},
                   'stash': [],
                   'sessionmaker': MagicMock()}

        x = CompetitionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True
        x.get_argument = lambda *args: True
        x._validate = lambda *args: {'id': (1, 2), 'client_id': (1, 2), 'type': [CompetitionType.CLASSIFY]}
        x.get()
