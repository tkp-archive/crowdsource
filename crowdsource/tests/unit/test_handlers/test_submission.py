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

        x[0].userId = 0
        x[1].userId = 0
        x[2].userId = 0
        x[3].userId = 2
        x[4].userId = 2
        x[5].userId = 2

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

        context = {'users': {1234: ''},
                   'competitions': {1: x[0].competition},
                   'leaderboards': {},
                   'submissions': {0: x},
                   'stash': [],
                   'all_users': MagicMock(),
                   'all_competitions': MagicMock(),
                   'all_submissions': MagicMock(),
                   'sessionmaker': MagicMock()}

        x = SubmissionHandler(self.app, req, **context)
        x._transforms = []
        x.get_current_user = lambda: True
        x._validate = lambda *args, **kwargs: {'id': (1, 2), 'competition_id': (1, 2), 'user_id': (1, 2), 'type': CompetitionType.PREDICT}
        x.get()
