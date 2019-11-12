from mock import patch, MagicMock
import six
import cufflinks.datagen as cfdg
import pandas as pd
from datetime import datetime, timedelta
from sklearn.datasets import make_classification

from crowdsource.types.utils import _metric, checkAnswer, fetchDataset, answerPrototype
from crowdsource.persistence.models import Competition, Submission
from crowdsource.types.competition import CompetitionSpec
from crowdsource.types.submission import SubmissionSpec
from crowdsource.enums import CompetitionType, CompetitionMetric, DatasetFormat


def foo3(competitionSpec, *args, **kwargs):
    import pandas
    # import time
    from sklearn import linear_model
    data = competitionSpec.dataset

    answers = []

    if isinstance(competitionSpec.targets, dict):
        return
    targets = [competitionSpec.targets] if isinstance(competitionSpec.targets, six.string_types) else data.columns if competitionSpec.targets is None else competitionSpec.targets

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
    if isinstance(competitionSpec.dataset, six.string_types):
        dataset = fetchDataset(competitionSpec)
    else:
        return

    answer = answerPrototype(competitionSpec, dataset)
    return answer.fillna(0)


class TestUtils:
    def test_validateSpec(self):
        SubmissionSpec.validate(None, None, None)

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
        c2 = Competition.from_spec(1, competition)
        d2 = SubmissionSpec.from_dict({'competition_id': 2, 'answer': pd.DataFrame(dataset[1]).to_json(), 'answer_type': DatasetFormat.JSON})
        s = Submission.from_spec(1, 2, c2, d2)

        checkAnswer(s)

    def test_checkAnswer2(self):
        dataset = cfdg.ohlcv()
        competition = CompetitionSpec(title='',
                                      type=CompetitionType.PREDICT,
                                      expiration=datetime.now() + timedelta(minutes=1),
                                      prize=1.0,
                                      dataset=dataset.iloc[:-1],
                                      metric=CompetitionMetric.ABSDIFF,
                                      targets=dataset.columns[-1],
                                      answer=dataset.iloc[-1:],
                                      when=datetime.utcfromtimestamp(dataset[-1:].index.values[0].astype(datetime)/1000000000))

        c2 = Competition.from_spec(1, competition)
        ans = foo3(competition)
        print(ans)
        d2 = SubmissionSpec.from_dict({'competition_id': 2, 'answer': ans.to_json(), 'answer_type': DatasetFormat.JSON})
        s = Submission.from_spec(1, 2, c2, d2)

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

        c2 = Competition.from_spec(1, competition)
        ans = foo5(competition)
        s2 = SubmissionSpec.from_dict({'competition_id': 2, 'answer': ans.to_json(orient='records'), 'answer_type': DatasetFormat.JSON})
        s = Submission.from_spec(1, 2, c2, s2)

        checkAnswer(s)
