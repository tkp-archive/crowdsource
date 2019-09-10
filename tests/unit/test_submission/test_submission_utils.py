from mock import patch, MagicMock
import pandas as pd
import lantern as l
from crowdsource.submission.utils import validateSpec, _metric, checkAnswer
from crowdsource.structs import CompetitionStruct, SubmissionStruct
from datetime import datetime, timedelta
from sklearn.datasets import make_classification
from crowdsource.competition import CompetitionSpec
from crowdsource.utils import str_or_unicode
from crowdsource.utils.enums import CompetitionType, CompetitionMetric, DatasetFormat
from crowdsource.competition.utils import fetchDataset, answerPrototype


def foo3(competitionSpec, *args, **kwargs):
    from crowdsource.utils import log
    log.debug('Answering')

    import pandas
    # import time
    from sklearn import linear_model
    data = competitionSpec.dataset

    answers = []

    if isinstance(competitionSpec.targets, dict):
        return
    targets = [competitionSpec.targets] if str_or_unicode(competitionSpec.targets) else data.columns if competitionSpec.targets is None else competitionSpec.targets

    val = competitionSpec.when
    when = val.timestamp()

    # print(targets)

    for col in targets:
        reg = linear_model.LinearRegression()
        x = data[col].index.astype(int).values.reshape(len(data[col].index), 1)
        y = data[col].values.reshape(len(data[col]), 1)
        reg.fit(x, y)

        print('******************')
        answers.append(reg.predict([[when]])[0][0])

    answers.append(when)
    return pandas.DataFrame([answers], columns=targets+['when']).set_index(['when'])


def foo5(competitionSpec, *args, **kwargs):
    from crowdsource.utils import log
    log.debug('Answering')

    if str_or_unicode(competitionSpec.dataset):
        dataset = fetchDataset(competitionSpec)
    else:
        return

    answer = answerPrototype(competitionSpec, dataset)
    return answer.fillna(0)


class TestUtils:
    def test_validateSpec(self):
        validateSpec(None, None, None)

    def test_metric1(self):
        x = _metric(CompetitionMetric.LOGLOSS, pd.Series([1, 2]), pd.Series([2, 3]))
        print(x)
        assert x > 17
        assert x < 18

    def test_metric2(self):
        x = _metric(CompetitionMetric.ABSDIFF, pd.DataFrame([1]), pd.DataFrame([2]))
        print(x)
        assert x == -1

    def test_checkAnswer(self):
        dataset = make_classification()
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.CLASSIFY,
                                      expiration=datetime.now() + timedelta(minutes=1),
                                      prize=1.0,
                                      num_classes=2,
                                      dataset=pd.DataFrame(dataset[0]),
                                      metric=CompetitionMetric.LOGLOSS,
                                      answer=pd.DataFrame(dataset[1]))
        d = competition.to_dict()
        c2 = CompetitionStruct(1, 2, d)
        d2 = {'competitionId': 2, 'answer': pd.DataFrame(dataset[1]).to_json(), 'answer_type': DatasetFormat.JSON}
        s = SubmissionStruct(1, 2, 3, c2, d2, 1)

        checkAnswer(s)

    def test_checkAnswer2(self):
        dataset = l.ohlcv()
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=datetime.now() + timedelta(minutes=1),
                                      prize=1.0,
                                      dataset=dataset.iloc[:-1],
                                      metric=CompetitionMetric.ABSDIFF,
                                      targets=dataset.columns[-1],
                                      answer=dataset.iloc[-1:],
                                      when=datetime.utcfromtimestamp(dataset[-1:].index.values[0].astype(datetime)/1000000000))
        d = competition.to_dict()
        c2 = CompetitionStruct(1, 2, d)

        ans = foo3(CompetitionSpec.from_dict(d))

        print(ans)

        d2 = {'competitionId': 2, 'answer': ans.to_json(), 'answer_type': DatasetFormat.JSON}
        s = SubmissionStruct(1, 2, 3, c2, d2, 1)

        checkAnswer(s)

    def test_checkAnswer3(self):
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

        d = competition.to_dict()
        c2 = CompetitionStruct(1, 2, d)

        ans = foo5(CompetitionSpec.from_dict(d))

        d2 = {'competitionId': 2, 'answer': ans.to_json(orient='records'), 'answer_type': DatasetFormat.JSON}
        s = SubmissionStruct(1, 2, 3, c2, d2, 1)

        checkAnswer(s)
