import six
import pandas
import ujson
import validators
from traitlets import HasTraits
from ..enums import DatasetFormat


class SubmissionSpec(HasTraits):
    def __init__(self,
                 competitionId,
                 answer,
                 answer_type):
        SubmissionSpec.validate(competitionId, answer, answer_type)
        self.competitionId = competitionId
        self.answer = answer
        if isinstance(answer_type, six.string_types):
            answer_type = DatasetFormat(answer_type)
        self.answer_type = answer_type

    def to_dict(self):
        ret = {}
        ret['competitionId'] = self.competitionId
        if isinstance(self.answer, pandas.DataFrame):
            ret['answer'] = self.answer.to_json()
        else:
            ret['answer'] = self.answer
        ret['answer_type'] = self.answer_type.value
        return ret

    def to_json(self):
        return ujson.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, val):
        d = {}
        for k, v in val.items():
            if k == 'answer_type':
                d[k] = DatasetFormat(v)
            elif k == 'answer':
                if not v or validators.url(v) or v == 'hidden':
                    d[k] = v
                else:
                    d[k] = pandas.DataFrame(ujson.loads(v))
            else:
                d[k] = v
        return cls(**d)

    @classmethod
    def from_json(cls, json):
        val = ujson.loads(json)
        return SubmissionSpec.from_dict(val)

    @staticmethod
    def validate(competitionId, answer, answer_type):
        pass