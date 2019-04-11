import ujson
import pandas as pd
import validators
from six import with_metaclass
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from .competition import CompetitionSpec
from .submission import SubmissionSpec
from .utils import str_or_unicode
from .utils.enums import DatasetFormat


class Struct(with_metaclass(ABCMeta)):
    @abstractmethod
    def to_dict(self):
        pass

    def to_json(self):
        return ujson.dumps(self.to_dict())

    def __repr__(self):
        return self.to_json()


class ClientStruct(Struct):
    '''Representation of a client

    Extends:
        Struct
    '''
    def __init__(self, id):
        self.id = id

    def to_dict(self):
        return {'id': self.id}


class CompetitionStruct(Struct):
    '''Representation of a competition spec

    Extends:
        Struct
    '''
    def __init__(self, id, clientId, spec):
        self.id = id
        self.clientId = clientId

        ##########################
        # load spec
        self.spec = CompetitionSpec.from_dict(spec)
        self.spec.expiration += timedelta(seconds=spec.get('answer_delay', 0))

        self.title = self.spec.title
        self.subtitle = self.spec.subtitle
        self.expiration = self.spec.expiration
        self.type = self.spec.type
        self.prize = self.spec.prize
        self.metric = self.spec.metric
        self.dataset = self.spec.dataset
        self.dataset_type = self.spec.dataset_type
        self.dataset_kwargs = self.spec.dataset_kwargs
        self.dataset_key = self.spec.dataset_key
        self.num_classes = self.spec.num_classes
        self.targets = self.spec.targets
        self.when = self.spec.when
        self.answer = self.spec.answer if str_or_unicode(self.spec.answer) and validators.url(self.spec.answer) else self.spec.answer if isinstance(self.spec.answer, pd.DataFrame) else '' if not self.spec.answer else pd.DataFrame(ujson.loads(self.spec.answer))
        self.answer_type = self.spec.dataset_type if self.spec.answer_type == DatasetFormat.NONE else self.spec.answer_type
        self.answer_delay = self.spec.answer_delay
        ##########################

        # Logic for whether to query for answer or calculate immediately
        self.current_state = pd.DataFrame()

        # is active?
        self.active = datetime.now() < self.spec.expiration

        # creation timestamp
        self.timestamp = datetime.now()

    def to_dict(self, private=False):
        x = self.spec.to_dict()
        x['id'] = self.id
        x['clientId'] = self.clientId
        x['active'] = self.active
        x['expiration'] = self.expiration.strftime("%Y-%m-%d %H:%M:%S")
        x['timestamp'] = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # hide if private
        if private:
            x['answer'] = self.answer if str_or_unicode(self.answer) else self.answer.to_json()
        else:
            x['answer'] = 'hidden'
        return x

    def __lt__(self, other):
        return self.expiration < other.expiration


class SubmissionStruct(Struct):
    '''Represenation of a submission

    Extends:
        Struct
    '''
    def __init__(self, id, clientId, competitionId, competition, spec, score):
        self.id = id
        self.clientId = clientId
        self.competitionId = competitionId
        self.score = score

        self.competition = competition  # dont include in dict

        ##########################
        # load spec
        self.spec = SubmissionSpec.from_dict(spec)
        self.answer = self.spec.answer if str_or_unicode(self.spec.answer) and validators.url(self.spec.answer) else self.spec.answer if isinstance(self.spec.answer, pd.DataFrame) else '' if not self.spec.answer else pd.DataFrame(ujson.loads(self.spec.answer))
        self.answer_type = self.spec.answer_type
        ##########################

        # is active?
        self.active = datetime.now() < self.competition.spec.expiration

        # creation timestamp
        self.timestamp = datetime.now()

    def to_dict(self, private=False):
        x = self.spec.to_dict()
        x['id'] = self.id
        x['clientId'] = self.clientId

        x['active'] = datetime.now() < self.competition.spec.expiration
        x['timestamp'] = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # helpful from competition
        x['type'] = self.competition.spec.type.value
        x['score'] = self.score
        x['expiration'] = self.competition.spec.expiration.strftime("%Y-%m-%d %H:%M:%S")
        x['metric'] = self.competition.spec.metric.value

        # hide if private
        if private:
            x['answer'] = self.answer if str_or_unicode(self.answer) else self.answer.to_json()
        else:
            x['answer'] = 'hidden'

        return x

    def __lt__(self, other):
        return abs(self.score) < abs(other.score)
