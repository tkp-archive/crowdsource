from mock import MagicMock, patch
from crowdsource.types.competition import CompetitionSpec
from crowdsource.types.utils import fetchDataset, _fetchDataset, answerPrototype
from crowdsource.enums import CompetitionType, CompetitionMetric, DatasetFormat
from crowdsource.exceptions import MalformedDataType, MalformedMetric, MalformedCompetition, MalformedTargets, MalformedDataset
from datetime import datetime, timedelta
from sklearn.datasets import make_classification
import cufflinks.datagen as cfdg
import pandas as pd
import numpy as np


class TestUtils:
    def test_validateSpec(self):
        CompetitionSpec.validate('', '', CompetitionType.CLASSIFY, None, 1.0, CompetitionMetric.LOGLOSS, 'http://test.com', 'test', DatasetFormat.JSON, None, None, 2, None, '', None, '')

        try:
            CompetitionSpec.validate('', '', None, None, 1.0, CompetitionMetric.LOGLOSS, 'http://test.com', 'test', DatasetFormat.JSON, None, None, 2, None, '', None, '')
            assert False
        except MalformedCompetition:
            pass

        try:
            CompetitionSpec.validate('', '', CompetitionType.CLASSIFY, None, 1.0, None, 'http://test.com', 'test', DatasetFormat.JSON, None, None, 2, None, '', None, '')
            assert False
        except MalformedMetric:
            pass

        try:
            CompetitionSpec.validate('', '', CompetitionType.CLASSIFY, None, 1.0, CompetitionMetric.LOGLOSS, 'http://test.com', 'test', None, None, None, 2, None, '', None, '')
            assert False
        except MalformedDataset:
            pass

        try:
            CompetitionSpec.validate('', '', CompetitionType.PREDICT, None, 1.0, CompetitionMetric.LOGLOSS, 'http://test.com', None, DatasetFormat.JSON, None, None, 2, None, '', None, '')
            assert False
        except MalformedTargets:
            pass

    def test_fetchDataset(self):
        x = _fetchDataset(pd.DataFrame(), None)
        assert x.empty

        with patch('requests.get') as m:
            m.return_value.status_code = 200
            m.return_value.text = '{}'
            _fetchDataset('', DatasetFormat.CSV)
        with patch('requests.get') as m:
            m.return_value.status_code = 200
            m.return_value.text = '{}'
            m.return_value.json = MagicMock(return_value={"test": [5]})
            _fetchDataset('', DatasetFormat.JSON)
        with patch('requests.get') as m:
            m.return_value = MagicMock()
            m.return_value.status_code = 200
            m.return_value.text = '{"test":[5]}'
            m.return_value.json = MagicMock(return_value={"test": [5]})
            _fetchDataset('', DatasetFormat.JSON, 'test')
        try:
            _fetchDataset('', 3)
            assert False
        except MalformedDataType:
            pass

    def test_answerPrototype1(self):
        # AnswerType.ONE
        dataset = make_classification()
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.CLASSIFY,
                                      expiration=datetime.now() + timedelta(minutes=1),
                                      prize=1.0,
                                      num_classes=2,
                                      dataset=pd.DataFrame(dataset[0]),
                                      metric=CompetitionMetric.LOGLOSS,
                                      answer=pd.DataFrame(dataset[1]))

        dataset = fetchDataset(competition)
        df = answerPrototype(competition)
        ans = pd.DataFrame([{'class': np.nan} for x in dataset.index])
        print(df)
        print(ans)
        assert df.equals(ans)

    def test_answerPrototype2(self):
        # AnswerType.TWO
        exp = datetime.now() + timedelta(minutes=2)
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=exp,
                                      when=exp,
                                      prize=1.0,
                                      dataset='http://bonds.paine.nyc',
                                      dataset_type=DatasetFormat.JSON,
                                      metric=CompetitionMetric.ABSDIFF,
                                      dataset_key='Name',
                                      targets={'ABC Corp': ['Price']})
        df = answerPrototype(competition)[['Price', 'when']]
        ans = pd.DataFrame([{'when': exp, 'Price': np.nan}], index=['ABC Corp'])[['Price', 'when']]
        print(df)
        print(ans)
        assert df.equals(ans)

    def test_answerPrototype3(self):
        # AnswerType.THREE
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=datetime.now() + timedelta(minutes=1),
                                      prize=1.0,
                                      dataset='http://bonds.paine.nyc',
                                      dataset_type=DatasetFormat.JSON,
                                      metric=CompetitionMetric.ABSDIFF,
                                      dataset_key='Name',
                                      targets={'ABC Corp': ['Price']})
        dataset = fetchDataset(competition)
        df = answerPrototype(competition, dataset)
        index = dataset[dataset['Name'] == 'ABC Corp'].index
        ans = pd.DataFrame([{'Name': 'ABC Corp', 'Price': np.nan} for _ in index], index=index)
        print(df)
        print(ans)
        assert df.equals(ans)

    def test_answerPrototype4(self):
        # AnswerType.FOUR
        exp = datetime.now() + timedelta(minutes=2)
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=exp,
                                      when=exp,
                                      prize=1.0,
                                      dataset='http://bonds.paine.nyc',
                                      dataset_type=DatasetFormat.JSON,
                                      metric=CompetitionMetric.ABSDIFF,
                                      targets={0: ['Price']})
        df = answerPrototype(competition)[['Price']]
        ans = pd.DataFrame([{'when': exp, 'Price': np.nan}], index=[0])[['Price']]
        print(df)
        print(ans)
        assert df.equals(ans)

    def test_answerPrototype5(self):
        # AnswerType.FIVE
        exp = datetime.now() + timedelta(minutes=2)
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=exp,
                                      prize=1.0,
                                      dataset='http://bonds.paine.nyc',
                                      dataset_type=DatasetFormat.JSON,
                                      metric=CompetitionMetric.ABSDIFF,
                                      targets={0: ['Price']})
        df = answerPrototype(competition)
        ans = pd.DataFrame([{'Price': np.nan}])
        print(df)
        print(ans)
        assert df.equals(ans)

    def test_answerPrototype6(self):
        # AnswerType.SIX
        dataset = cfdg.ohlcv().reset_index()
        exp = datetime.utcfromtimestamp(dataset[-1:]['index'].values[0].astype(datetime)/1000000000)
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=datetime.now() + timedelta(minutes=1),
                                      prize=1.0,
                                      dataset=dataset.iloc[:-1],
                                      metric=CompetitionMetric.ABSDIFF,
                                      targets=dataset.columns[-1],
                                      answer=dataset.iloc[-1:],
                                      dataset_key='index',
                                      when=exp)

        df = answerPrototype(competition)[['when', dataset.columns[-1]]]
        ans = pd.DataFrame([{'when': exp, dataset.columns[-1]: np.nan} for x in dataset['index'].iloc[:-1]], index=[x for x in dataset['index'].iloc[:-1]])[['when', dataset.columns[-1]]]
        print(df)
        print(ans)
        assert df.equals(ans)

    def test_answerPrototype62(self):
        # AnswerType.SIX
        exp = datetime.now() + timedelta(minutes=2)
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      when=exp,
                                      prize=1.0,
                                      dataset='https://feeds.citibikenyc.com/stations/stations.json',
                                      dataset_type=DatasetFormat.JSON,
                                      dataset_key='id',
                                      dataset_kwargs={'record_column': 'stationBeanList'},
                                      metric=CompetitionMetric.ABSDIFF,
                                      targets=['availableBikes', 'availableDocks'],
                                      expiration=exp)

        dataset = fetchDataset(competition)
        df = answerPrototype(competition)[['when', 'availableBikes', 'availableDocks']]
        ans = pd.DataFrame([{'when': exp, 'availableBikes': np.nan, 'availableDocks': np.nan} for x in dataset.id], index=[id for id in dataset.id])[['when', 'availableBikes', 'availableDocks']]
        print(df)
        print(ans)
        assert df.equals(ans)

    def test_answerPrototype7(self):
        # AnswerType.SEVEN
        dataset = cfdg.ohlcv().reset_index()
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=datetime.now() + timedelta(minutes=1),
                                      prize=1.0,
                                      dataset=dataset.iloc[:-1],
                                      metric=CompetitionMetric.ABSDIFF,
                                      targets=dataset.columns[-1],
                                      dataset_key='index',
                                      answer=dataset.iloc[-1:])

        df = answerPrototype(competition)
        ans = pd.DataFrame([{dataset.columns[-1]: np.nan} for x in dataset['index'].iloc[:-1]], index=dataset['index'].iloc[:-1])
        print(df)
        print(ans)
        assert df.equals(ans)

    def test_answerPrototype8(self):
        # AnswerType.EIGHT
        dataset = cfdg.ohlcv()
        exp = datetime.utcfromtimestamp(dataset[-1:].index.values[0].astype(datetime)/1000000000)
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=datetime.now() + timedelta(minutes=1),
                                      prize=1.0,
                                      dataset=dataset.iloc[:-1],
                                      metric=CompetitionMetric.ABSDIFF,
                                      targets=dataset.columns[-1],
                                      answer=dataset.iloc[-1:],
                                      when=exp)

        df = answerPrototype(competition)
        ans = pd.DataFrame([{dataset.columns[-1]: np.nan}], index=[exp])
        print(df)
        print(ans)
        assert df.equals(ans)

    def test_answerPrototype9(self):
        # AnswerType.NINE
        dataset = cfdg.ohlcv()
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=datetime.now() + timedelta(minutes=1),
                                      prize=1.0,
                                      dataset=dataset.iloc[:-1],
                                      metric=CompetitionMetric.ABSDIFF,
                                      targets=dataset.columns[-1],
                                      answer=dataset.iloc[-1:])

        df = answerPrototype(competition)
        ans = pd.DataFrame([{dataset.columns[-1]: np.nan} for x in dataset.index])
        ans = pd.DataFrame([{dataset.columns[-1]: np.nan}])
        print(df)
        print(ans)
        assert df.equals(ans)
