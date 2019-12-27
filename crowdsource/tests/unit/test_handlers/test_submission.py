import tornado.web
from datetime import datetime
from crowdsource.handlers import SubmissionHandler
from crowdsource.enums import CompetitionType
from mock import MagicMock
from tornado.web import HTTPError


class TestSubmissions:
    def setup(self):
        self.app = tornado.web.Application(cookie_secret='test')
        self.app._transforms = []

    def test_SubmissionHandler(self):
        req = MagicMock()
        req.body = ''

        z = MagicMock()
        z.expiration = datetime(2020, 1, 1)
        sessionmaker = MagicMock()
        sessionmaker.return_value.query.return_value.filter_by.return_value.first.return_value = z

        context = {'clients': {1234: ''},
                   'competitions': {1234: z},
                   'leaderboards': {},
                   'submissions': {},
                   'stash': [],
                   'sessionmaker': sessionmaker}

        x = SubmissionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True

        # requires client id
        x.get()
        try:
            x.post()
            assert False
        except HTTPError:
            pass
        assert(x.get_status() == 400)

        # unregistered
        req.body = '{"id":1233}'
        x = SubmissionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True
        try:
            x.post()
            assert False
        except HTTPError:
            pass

        assert(x.get_status() == 400)

        # no competition id
        req.body = '{"id":1234}'
        x = SubmissionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True
        try:
            x.post()
            assert False
        except HTTPError:
            pass

        assert(x.get_status() == 400)

        # no submission
        req.body = '{"id":1234, "competition_id":1234}'
        x = SubmissionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True
        try:
            x.post()
            assert False
        except HTTPError:
            pass

        assert(x.get_status() == 400)

        # malformed submission
        req.body = '{"id":1234, "competition_id":1234, "submission": "{}"}'
        x = SubmissionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True
        try:
            x.post()
            assert False
        except HTTPError:
            pass

        assert(x.get_status() == 400)

    def test_submissions(self):
        req = MagicMock()
        req.body = ''
        x = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        x[0].id = 0
        x[1].id = 1
        x[2].id = 1
        x[3].id = 2
        x[4].id = 2
        x[5].id = 2

        x[0].competitionId = 0
        x[1].competitionId = 0
        x[2].competitionId = 1
        x[3].competitionId = 1
        x[4].competitionId = 2
        x[5].competitionId = 2

        x[0].clientId = 0
        x[1].clientId = 0
        x[2].clientId = 0
        x[3].clientId = 2
        x[4].clientId = 2
        x[5].clientId = 2

        x[0].competition.spec.type = CompetitionType.CLASSIFY
        x[1].competition.spec.type = CompetitionType.CLASSIFY
        x[2].competition.spec.type = CompetitionType.CLASSIFY
        x[3].competition.spec.type = CompetitionType.CLASSIFY
        x[4].competition.spec.type = CompetitionType.PREDICT
        x[5].competition.spec.type = CompetitionType.PREDICT

        x[0].competition.expiration = datetime(2020, 1, 1)
        x[1].competition.expiration = datetime(2020, 1, 1)
        x[2].competition.expiration = datetime(2020, 1, 1)
        x[3].competition.expiration = datetime(2020, 1, 1)
        x[4].competition.expiration = datetime(2020, 1, 1)
        x[5].competition.expiration = datetime(2020, 1, 1)

        x[0].to_dict = lambda *args, **kwargs: {'score': 1}
        x[1].to_dict = lambda *args, **kwargs: {'score': 1}
        x[2].to_dict = lambda *args, **kwargs: {'score': 1}
        x[3].to_dict = lambda *args, **kwargs: {'score': 1}
        x[4].to_dict = lambda *args, **kwargs: {'score': 1}
        x[5].to_dict = lambda *args, **kwargs: {'score': 1}

        context = {'clients': {1234: ''},
                   'competitions': {1: x[0].competition},
                   'leaderboards': {},
                   'submissions': {0: x},
                   'stash': [],
                   'sessionmaker': MagicMock()}

        x = SubmissionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True
        x._validate = lambda *args, **kwargs: {'id': (1, 2), 'competition_id': (1, 2), 'client_id': (1, 2), 'type': CompetitionType.PREDICT}
        x.get()
