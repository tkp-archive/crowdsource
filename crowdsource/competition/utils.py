import numpy as np
import pandas as pd
import requests
from six import StringIO
import validators
from pandas.io.json import json_normalize
from ..utils import str_or_unicode
from ..utils.enums import CompetitionType, CompetitionMetric, DatasetFormat
from ..utils.exceptions import MalformedDataType, MalformedCompetition, MalformedMetric, MalformedDataset, MalformedTargets


def validateSpec(title,
                 subtitle,
                 type,
                 expiration,
                 prize,
                 metric,
                 dataset,
                 targets,
                 dataset_type,
                 dataset_kwargs,
                 dataset_key,
                 num_classes,
                 when,
                 answer,
                 answer_type,
                 answer_delay):

    if not isinstance(type, CompetitionType):
        raise MalformedCompetition()

    if not isinstance(metric, CompetitionMetric):
        raise MalformedMetric()

    if str_or_unicode(dataset) and validators.url(dataset):
        if not isinstance(dataset_type, DatasetFormat):
            raise MalformedDataset()

    if type == CompetitionType.PREDICT:
        if targets is None:
            raise MalformedTargets()


def _fetchDataset(data, data_type, record_column='', cookies=None, proxies=None, **kwargs):
    '''Must be pandas readable'''
    if isinstance(data, pd.DataFrame):
        return data
    if data_type == DatasetFormat.CSV:
        resp = requests.get(data, cookies=cookies, proxies=proxies)
        if resp.status_code != 200:
            raise MalformedDataset()
        return pd.read_csv(StringIO(resp.text))
    elif data_type == DatasetFormat.JSON:
        resp = requests.get(data, cookies=cookies, proxies=proxies)
        if resp.status_code != 200:
            raise MalformedDataset()

        if record_column:
            df1 = pd.DataFrame(resp.json())
            df2 = json_normalize(resp.json(), record_column)
            return pd.concat([df1, df2], axis=1, join='inner')
        return pd.read_json(StringIO(resp.text))
    else:
        raise MalformedDataType(data_type)


def fetchDataset(spec):
    dataset_url = spec.dataset
    dataset_url_type = spec.dataset_type
    return _fetchDataset(dataset_url, dataset_url_type, **spec.dataset_kwargs)


def answerPrototype(spec, dataset=None):
    if dataset is None or str_or_unicode(dataset):
        dataset = fetchDataset(spec)

    type = spec.type
    targets = spec.targets

    key = spec.dataset_key
    when = spec.when

    if type == CompetitionType.CLASSIFY:
        # AnswerType.ONE
        df = pd.DataFrame(index=dataset.index)
        df['class'] = pd.Series()

    elif type == CompetitionType.PREDICT:
        '''
             ____________________________________________________
            |   target type     key       when      predicting   |
            |____________________________________________________|
            |   dictionary   |  yes   |   yes  |   df[df[key] == k][v] for k,v in targets.items() as of time when
            |   dictionary   |  yes   |   no   |   df[df[key] == k][v] for k,v in targets.items()
            |   dictionary   |  no    |   yes  |   df[df.index==k][v] for k,v in targets.items() as of time when
            |   dictionary   |  no    |   no   |   df[df.index==k][v] for k,v in targets.items()
            |   list         |  yes   |   yes  |   df[df[key] == v] for v in targets as of time when
            |   list         |  yes   |   no   |   df[df[key] == v] for v in targets
            |   list         |  no    |   yes  |   df[targets] as of time when
            |   list         |  no    |   no   |   df[targets]
            |____________________________________________________

            if targets is dictionary:
                if key:
                    for k, v in targets:
                        if when:
                            e.g. samples.predictCorporateBonds
                                    when      k1-v1     k1-v2  k2-v1
                            k1      when       NaN        NaN    NaN
                            k2      when       NaN        NaN    NaN

                        else:
                            e.g. none yet
                                   k1-v1     k1-v2  k2-v1
                            k1      NaN        NaN    NaN
                            k2      NaN        NaN    NaN

                else:
                    for k, v in targets:
                        if when:
                            e.g. none yet (keys need not overlap)
                                   when   k1-v1   k1-v2   k3-v1
                            k1     when    NaN     NaN     NaN
                            k3     when    NaN     NaN     NaN

                        else:
                            e.g. none yet
                                  k1-v1   k1-v2   k2-v1
                            k1     NaN     NaN     NaN
                            k3     NaN     NaN     NaN


            if targets is string:
                targets = [targets]

            if targets is list:
                if key:
                    if when:
                        e.g. none yet
                                when      target1      target2
                            1   when        NaN          NaN
                            2   when        NaN          NaN

                    else:
                        e.g. samples.predictCitibike
                            key        target1    target2
                            72           NaN        NaN
                            79           NaN        NaN


                else:
                    if when:
                        e.g. samples.predict1 and samples.predict2
                            0   when  target1  target2
                            1   when   NaN      NaN


                    else:
                        e.g. none yet (means next tick)
                               target1  target2
                            0   NaN      NaN
        '''

        if isinstance(targets, dict):
            if key:
                if when:
                    # AnswerType.TWO
                    keys = list(targets.keys())
                    df = pd.DataFrame([{'when': spec.when} for _ in keys], index=keys)
                    for k, v in targets.items():
                        for item in v:
                            df[item] = pd.Series()

                else:
                    # AnswerType.THREE
                    keys = list(targets.keys())

                    df = pd.DataFrame(dataset[dataset[key].isin(keys)][key], index=dataset[dataset[key].isin(keys)].index)

                    vals = list(set([v for x in list(targets.values()) for v in x]))
                    for val in vals:
                        df[val] = pd.Series()

            else:
                if when:
                    # AnswerType.FOUR
                    keys = list(targets.keys())
                    df = pd.DataFrame([{'when': spec.when} for _ in keys], index=keys)
                    for k, v in targets.items():
                        for item in v:
                            df[item] = pd.Series()

                else:
                    # AnswerType.FIVE
                    keys = list(targets.keys())
                    vals = list(set([v for x in list(targets.values()) for v in x]))

                    df = pd.DataFrame([{v: np.nan for v in vals} for _ in keys], index=keys)

        else:
            if str_or_unicode(targets):
                targets = [targets]

            if not isinstance(targets, list):
                raise Exception()  # TODO

            if key:
                if when:
                    # AnswerType.SIX
                    df = pd.DataFrame([{'when': when} for x in dataset[key]], index=dataset[key])
                    for item in targets:
                        df[item] = pd.Series()

                else:
                    # AnswerType.SEVEN
                    df = pd.DataFrame([{x: np.nan for x in targets} for _ in dataset[key]], index=dataset[key])

            else:
                if when:
                    # AnswerType.EIGHT
                    df = pd.DataFrame([{x: np.nan for x in targets}], index=[spec.when])

                else:
                    # AnswerType.NINE
                    df = pd.DataFrame([np.nan for _ in targets], columns=targets)

    elif type == CompetitionType.CLUSTER:
        # AnswerType.TEN
        raise NotImplemented()

    return df
