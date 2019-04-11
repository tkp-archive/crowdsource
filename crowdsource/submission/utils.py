import pandas as pd
from ..competition.utils import _fetchDataset
from ..utils import str_or_unicode
from ..utils.enums import CompetitionType, CompetitionMetric
from sklearn.metrics import log_loss


def validateSpec(competitionId, answer, answer_type):
    pass


def _metric(metric, x, y, **kwargs):
    if metric == CompetitionMetric.LOGLOSS:
        return log_loss(x.values, y.values, **kwargs)
    else:
        return (x.values-y.values).sum(1)[0]


def checkAnswer(submission):
    competition = submission.competition

    # Competition answer #
    answer = competition.answer
    answer_type = competition.answer_type
    dataset_kwargs = competition.dataset_kwargs

    # grab answer if possible
    if str_or_unicode(answer):
        real_answer = _fetchDataset(answer, answer_type, **dataset_kwargs)
    else:
        real_answer = pd.DataFrame(answer)
    ####

    # user answer #
    user_answer = submission.answer
    user_answer_type = submission.answer_type

    # grab user answer if possible
    if str_or_unicode(user_answer):
        real_user_answer = _fetchDataset(user_answer, user_answer_type, **dataset_kwargs)
    else:
        real_user_answer = pd.DataFrame(user_answer)
    ####

    if competition.type == CompetitionType.CLASSIFY:
        return _metric(competition.metric, real_answer, real_user_answer, eps=1e-15)

    elif competition.type == CompetitionType.PREDICT:
        if isinstance(competition.targets, list):
            real_answer = real_answer[competition.targets]
            real_user_answer = real_user_answer[competition.targets]
        elif isinstance(competition.targets, dict):
            keyfield = competition.dataset_key
            keys = list(set(competition.targets.keys()))  # TODO more than 1 key?
            columns = list(set([v for x in competition.targets.values() for v in x]))
            real_answer = real_answer[real_answer[keyfield].isin(keys)][columns]
            real_user_answer = real_user_answer[real_user_answer[keyfield].isin(keys)][columns]
        elif isinstance(competition.targets, list):
            real_answer = real_answer[competition.targets]
            real_user_answer = real_user_answer[competition.targets]
        else:
            real_answer = real_answer[[competition.targets]]
            real_user_answer = real_user_answer[[competition.targets]]
        return _metric(competition.metric, real_answer, real_user_answer, eps=1e-15)

    elif competition.type == CompetitionType.CLUSTER:
        return _metric(competition.metric, real_answer, real_user_answer, eps=1e-15)

    return 0.0
