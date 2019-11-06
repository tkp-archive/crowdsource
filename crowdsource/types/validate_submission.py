from ..utils.enums import CompetitionMetric
from sklearn.metrics import log_loss


def validateSpec(competitionId, answer, answer_type):
    pass


def _metric(metric, x, y, **kwargs):
    if metric == CompetitionMetric.LOGLOSS:
        return log_loss(x.values, y.values, **kwargs)
    else:
        return (x.values-y.values).sum(1)[0]
