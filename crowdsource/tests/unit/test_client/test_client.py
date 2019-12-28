import pandas
import ujson
from datetime import datetime, timedelta
from sklearn.datasets import make_classification
from crowdsource.client import Client
from mock import patch, MagicMock
from crowdsource.types.competition import CompetitionSpec
from crowdsource.enums import CompetitionType, CompetitionMetric


dataset = make_classification()
competition = CompetitionSpec(title='',
                              type=CompetitionType.CLASSIFY,
                              expiration=datetime.now() + timedelta(minutes=1),
                              prize=1.0,
                              num_classes=2,
                              dataset=pandas.DataFrame(dataset[0]),
                              metric=CompetitionMetric.LOGLOSS,
                              answer=pandas.DataFrame(dataset[1]))


class TestClient:
    def test_init(self):
        with patch('requests.post') as m:
            m.return_value = MagicMock()
            m.return_value.text = '{"id":1}'
            c = Client('test')
            assert(c)

    def test_register(self):
        with patch('requests.post') as m:
            m.return_value = MagicMock()
            m.return_value.text = '{"id":1}'
            c = Client('test')

        with patch('requests.post') as m:

            m.return_value = MagicMock()
            m.return_value.text = '{}'
            c.register()
            assert(not c._am_registered)

    def test_users(self):
        with patch('requests.post') as m:
            m.return_value = MagicMock()
            m.return_value.text = '{"id":1}'
            c = Client('test')

        with patch('requests.get') as mock:
            mock.return_value = MagicMock()
            mock.return_value.text = ujson.dumps({'test': 'test'})
            c.register = lambda: None
            x = c.users()
            assert(x == {'test': 'test'})

    def test_start_competition(self):
        with patch('requests.post') as m:
            m.return_value = MagicMock()
            m.return_value.text = '{"id":1}'
            c = Client('test')

        with patch('requests.post') as mock:
            c.register = lambda: None
            mock.return_value = MagicMock()
            mock.return_value.text = '[]'
            c.start_competition(competition)
            assert(c._my_competitions[0] == [])

    def test_compete(self):
        pass

    def test_sampleClassify(self):
        with patch('requests.post') as m:
            m.return_value = MagicMock()
            m.return_value.text = '{"id":1}'
            c = Client('test')

        with patch('requests.post') as mock:
            c.register = lambda: None
            mock.return_value = MagicMock()
            mock.return_value.text = '{"id":1}'
            c._sampleClassify1()
            assert(c._my_competitions[0] == {'id': 1})

    def test_samplePredict1(self):
        with patch('requests.post') as m:
            m.return_value = MagicMock()
            m.return_value.text = '{"id":1}'
            c = Client('test')

        with patch('requests.post') as mock:
            c.register = lambda: None
            mock.return_value = MagicMock()
            mock.return_value.text = '{"id":1}'
            c._samplePredict1()
            assert(c._my_competitions[0] == {'id': 1})

    def test_samplePredict2(self):
        with patch('requests.post') as m:
            m.return_value = MagicMock()
            m.return_value.text = '{"id":1}'
            c = Client('test')

        with patch('requests.post') as mock:
            mock.return_value = MagicMock()
            mock.return_value.text = '{"id":1}'
            c._samplePredict2()
            assert(c._my_competitions[0] == {'id': 1})

    def leaderboards(self):
        with patch('requests.post') as m:
            m.return_value = MagicMock()
            m.return_value.text = '{"id":1}'
            c = Client('test')

        with patch('requests.get') as mock:
            mock.return_value = MagicMock()
            mock.return_value.text = '[]'
            assert(c.leaderboards() == [])

    def test_submit(self):
        with patch('requests.post') as m:
            m.return_value = MagicMock()
            m.return_value.text = '{"id":1}'
            c = Client('test')

        with patch('requests.post') as mock:
            mock.return_value = MagicMock()
            mock.return_value.text = '{}'
            val = c.submit(MagicMock(), MagicMock())
            print(val)
            assert(val == {})
