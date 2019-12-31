import cufflinks.datagen as cfdg
import pandas
import time
import ujson
from datetime import datetime, timedelta
from sklearn.datasets import make_classification
from tornado_sqlalchemy_login.utils import safe_post, construct_path
from ..types.competition import CompetitionSpec
from ..enums import CompetitionType, CompetitionMetric, DatasetFormat


def classify1(host, cookies=None, proxies=None):
    dataset = make_classification()
    competition = CompetitionSpec(title='Classify this dataset',
                                  type=CompetitionType.CLASSIFY,
                                  expiration=datetime.now() + timedelta(minutes=1),
                                  prize=1.0,
                                  dataset=pandas.DataFrame(dataset[0]),
                                  metric=CompetitionMetric.LOGLOSS,
                                  answer=pandas.DataFrame(dataset[1]))
    resp = safe_post(construct_path(host, 'api/v1/competition'), data=ujson.dumps({'spec': competition.to_dict()}), cookies=cookies, proxies=proxies)
    return resp


def answerClassify1(competitionSpec, *args, **kwargs):
    import pandas
    data = competitionSpec.dataset
    ret = data[data.columns[0]] > kwargs.get('thresh', .5)
    return pandas.DataFrame(ret.astype(int))


def answerClassify2(competitionSpec, *args, **kwargs):
    return answerClassify1(competitionSpec, thresh=.2, *args, **kwargs)


def answerClassify3(competitionSpec, *args, **kwargs):
    import pandas
    data = competitionSpec.dataset
    ret = data[data.columns[0]] > kwargs.get('thresh', .7)
    return pandas.DataFrame(ret.astype(int))


def predict1(host, cookies=None, proxies=None):
    dataset = cfdg.ohlcv()
    competition = CompetitionSpec(title='Predict next day volume',
                                  type=CompetitionType.PREDICT,
                                  expiration=datetime.now() + timedelta(minutes=1),
                                  prize=1.0,
                                  dataset=dataset.iloc[:-1],
                                  metric=CompetitionMetric.ABSDIFF,
                                  targets=dataset.columns[-1],
                                  answer=dataset.iloc[-1:],
                                  when=datetime.utcfromtimestamp(dataset[-1:].index.values[0].astype(datetime) / 1000000000))
    resp = safe_post(construct_path(host, 'api/v1/competition'), data=ujson.dumps({'spec': competition.to_dict()}), cookies=cookies, proxies=proxies)
    return resp


def predict2(host, cookies=None, proxies=None):
    dataset = cfdg.lines()
    competition = CompetitionSpec(title='Predict future value',
                                  type=CompetitionType.PREDICT,
                                  expiration=datetime.now() + timedelta(minutes=1),
                                  prize=1.0,
                                  dataset=dataset.iloc[:-1],
                                  metric=CompetitionMetric.ABSDIFF,
                                  answer=dataset.iloc[-1:],
                                  targets=dataset.columns,
                                  when=datetime.utcfromtimestamp(dataset[-1:].index.values[0].astype(datetime) / 1000000000))
    resp = safe_post(construct_path(host, 'api/v1/competition'), data=ujson.dumps({'spec': competition.to_dict()}), cookies=cookies, proxies=proxies)
    return resp


def answerPredict1(competitionSpec, *args, **kwargs):
    from crowdsource.types.utils import answerPrototype, fetchDataset
    from sklearn import linear_model

    data = fetchDataset(competitionSpec)

    ans = answerPrototype(competitionSpec, data)
    when = competitionSpec.when
    if not when or competitionSpec.dataset_key:
        ''' TS prediction'''
        return

    for col in ans.columns:
        if col == competitionSpec.dataset_key:
            continue
        reg = linear_model.LinearRegression()
        x = data[col].index.astype(int).values.reshape(len(data[col].index), 1)
        y = data[col].values.reshape(len(data[col]), 1)
        reg.fit(x, y)

        ans.loc[when, col] = reg.predict([[when.timestamp() if hasattr(when, 'timestamp') else float((time.mktime(when.timetuple()) + when.microsecond / 1000000.0))]])

    return ans


def predictCorporateBonds(host, cookies=None, proxies=None):
    competition = CompetitionSpec(title='Predict corporate bond volume',
                                  type=CompetitionType.PREDICT,
                                  expiration=datetime.now() + timedelta(minutes=1),
                                  prize=1.0,
                                  dataset='http://bonds.paine.nyc',
                                  dataset_type=DatasetFormat.JSON,
                                  metric=CompetitionMetric.ABSDIFF,
                                  dataset_key='Name',
                                  targets={'ABC Corp': ['Price']})
    resp = safe_post(construct_path(host, 'api/v1/competition'), data=ujson.dumps({'spec': competition.to_dict()}), cookies=cookies, proxies=proxies)
    return resp


def answerPredictCorporateBonds(competitionSpec, *args, **kwargs):
    from random import normalvariate
    from crowdsource.types.utils import answerPrototype, fetchDataset

    dataset = fetchDataset(competitionSpec)
    answer = answerPrototype(competitionSpec, dataset)

    if competitionSpec.when or not competitionSpec.dataset_key:
        '''next val prediction'''
        return

    for i in answer.index:
        for col in answer.columns:
            if col == competitionSpec.dataset_key:
                continue
            ran = normalvariate(0, 5.0)
            answer.loc[i, col] = dataset.loc[i, col] + ran

    return answer


def predictCitibike(host, cookies=None, proxies=None):
    exp = datetime.now() + timedelta(minutes=2)
    competition = CompetitionSpec(title='Predict citibike volume',
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
    resp = safe_post(construct_path(host, 'api/v1/competition'), data=ujson.dumps({'spec': competition.to_dict()}), cookies=cookies, proxies=proxies)
    return resp


def answerPredictCitibike(competitionSpec, *args, **kwargs):
    from random import randint
    from crowdsource.types.utils import answerPrototype, fetchDataset

    dataset = fetchDataset(competitionSpec)
    answer = answerPrototype(competitionSpec, dataset)

    when = competitionSpec.when

    if not when or not competitionSpec.dataset_key:
        ''' TS prediction'''
        return

    for i in answer.index:
        for col in answer.columns:
            if col == 'when':
                continue

            ran = randint(0, 10)
            answer.loc[i, col] = dataset[dataset[competitionSpec.dataset_key] == i][col].iloc[0] + ran

    return answer
