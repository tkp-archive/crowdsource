import time
from datetime import datetime

import pandas
import six
import ujson
import validators
from traitlets import HasTraits

from ..enums import CompetitionMetric, CompetitionType, DatasetFormat
from ..exceptions import (MalformedCompetition, MalformedDataset,
                          MalformedMetric, MalformedTargets)


class CompetitionSpec(HasTraits):
    def __init__(
        self,
        title,
        type,
        expiration,
        prize,
        metric,
        dataset,
        subtitle="",
        targets=None,
        dataset_type=DatasetFormat.NONE,
        dataset_kwargs=None,
        dataset_key=None,
        num_classes=2,
        when=None,
        answer=None,
        answer_type=DatasetFormat.NONE,
        answer_delay=0,
    ):
        CompetitionSpec.validate(
            title,
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
            answer_delay,
        )
        self.title = title
        self.subtitle = subtitle
        self.type = type
        self.expiration = expiration
        self.prize = prize
        self.metric = metric

        # provide dataset if available
        self.dataset = dataset

        if isinstance(dataset, six.string_types) and validators.url(dataset):
            self.dataset_type = dataset_type
        else:
            self.dataset_type = DatasetFormat.NONE

        self.dataset_kwargs = dataset_kwargs if dataset_kwargs else {}
        self.dataset_key = dataset_key

        self.num_classes = num_classes

        if type == CompetitionType.PREDICT:
            self.targets = targets
        else:
            self.targets = None

        self.when = when

        self.answer = answer
        if isinstance(answer, six.string_types) and validators.url(answer):
            self.answer_type = (
                self.dataset_type if answer_type == DatasetFormat.NONE else answer_type
            )
        else:
            self.answer_type = DatasetFormat.NONE

        self.answer_delay = answer_delay

    def to_dict(self):
        ret = {}
        ret["title"] = self.title
        ret["subtitle"] = self.subtitle
        ret["type"] = self.type.value
        ret["expiration"] = (
            self.expiration.timestamp()
            if hasattr(self.expiration, "timestamp")
            else float(
                (
                    time.mktime(self.expiration.timetuple())
                    + self.expiration.microsecond / 1000000.0
                )
            )
        )
        ret["prize"] = self.prize
        ret["metric"] = self.metric.value
        ret["dataset"] = (
            self.dataset
            if isinstance(self.dataset, six.string_types)
            else self.dataset.to_json()
        )
        ret["dataset_type"] = self.dataset_type.value
        ret["dataset_kwargs"] = self.dataset_kwargs
        ret["dataset_key"] = self.dataset_key
        ret["num_classes"] = self.num_classes
        ret["targets"] = list(self.targets) if self.targets is not None else None
        ret["when"] = (
            ""
            if self.when is None
            else self.when.timestamp()
            if hasattr(self.when, "timestamp")
            else float(
                (time.mktime(self.when.timetuple()) + self.when.microsecond / 1000000.0)
            )
        )
        ret["answer"] = (
            self.answer
            if isinstance(self.answer, six.string_types)
            else self.answer.to_json()
            if isinstance(self.answer, pandas.DataFrame)
            else self.dataset
        )
        ret["answer_delay"] = self.answer_delay
        return ret

    def to_json(self):
        return ujson.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, val):
        d = {}
        for k, v in val.items():
            if k == "type":
                d[k] = CompetitionType(v)
            elif k == "metric":
                d[k] = CompetitionMetric(v)
            elif k == "dataset_type" or k == "answer_type":
                d[k] = DatasetFormat(v)
            elif k == "dataset" or k == "answer":
                if isinstance(v, six.string_types):
                    if v in ("", "hidden") or validators.url(v):
                        d[k] = v
                    else:
                        v = ujson.loads(v)

                if isinstance(v, dict) or isinstance(v, list):
                    d[k] = pandas.DataFrame(v)
                else:
                    d[k] = v

            elif k == "expiration" or k == "when":
                if isinstance(v, six.string_types):
                    if not v:
                        d[k] = None
                    else:
                        d[k] = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                else:
                    if v:
                        d[k] = datetime.fromtimestamp(float(v))
            elif k in (
                "title",
                "subtitle",
                "prize",
                "dataset_kwargs",
                "dataset_key",
                "num_classes",
                "targets",
                "answer_delay",
            ):
                d[k] = v
        return cls(**d)

    @classmethod
    def from_json(cls, json):
        val = ujson.loads(json)
        return CompetitionSpec.from_dict(val)

    @staticmethod
    def validate(
        title,
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
        answer_delay,
    ):
        if not isinstance(type, CompetitionType):
            raise MalformedCompetition()

        if not isinstance(metric, CompetitionMetric):
            raise MalformedMetric()

        if isinstance(dataset, six.string_types) and validators.url(dataset):
            if not isinstance(dataset_type, DatasetFormat):
                raise MalformedDataset()

        if type == CompetitionType.PREDICT:
            if targets is None:
                raise MalformedTargets()

    def __repr__(self):
        return (
            "<title- "
            + str(self.title)
            + ", type-"
            + str(self.type.value)
            + ", expiration-"
            + str(self.expiration)
            + ", prize-"
            + str(self.prize)
            + ", dataset-"
            + str(self.dataset)
            + ", metric-"
            + str(self.metric.value)
            + ", num_classes-"
            + str(self.num_classes)
            + ", targets-"
            + str(self.targets)
            + ">"
        )
