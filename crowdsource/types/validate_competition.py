import validators
from ..utils import str_or_unicode
from ..utils.enums import CompetitionType, CompetitionMetric, DatasetFormat
from ..utils.exceptions import MalformedCompetition, MalformedMetric, MalformedDataset, MalformedTargets


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
