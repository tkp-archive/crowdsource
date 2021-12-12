import six
import pandas
import ujson
import validators
from traitlets import HasTraits
from ..enums import DatasetFormat


class SubmissionSpec(HasTraits):
    def __init__(self, competition_id, answer, answer_type):
        SubmissionSpec.validate(competition_id, answer, answer_type)
        self.competition_id = competition_id
        self.answer = answer
        if isinstance(answer_type, six.string_types):
            answer_type = DatasetFormat(answer_type)
        self.answer_type = answer_type

    def to_dict(self):
        ret = {}
        ret["competition_id"] = self.competition_id
        if isinstance(self.answer, pandas.DataFrame):
            ret["answer"] = self.answer.to_json()
        else:
            ret["answer"] = self.answer
        ret["answer_type"] = self.answer_type.value
        return ret

    def to_json(self):
        return ujson.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, val):
        d = {}
        for k, v in val.items():
            if k == "answer_type":
                d[k] = DatasetFormat(v)
            elif k == "answer":
                if isinstance(v, six.string_types):
                    if v in ("", "hidden") or validators.url(v):
                        d[k] = v
                    else:
                        v = ujson.loads(v)

                if isinstance(v, dict) or isinstance(v, list):
                    d[k] = pandas.DataFrame(v)
                else:
                    d[k] = v
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
