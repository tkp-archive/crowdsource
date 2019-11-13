import pandas as pd
import six
import secrets
import ujson
import validators
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

TOKEN_WIDTH = 64
Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    _email = Column("email", String, nullable=False, unique=True)

    apikeys = relationship('APIKey', back_populates='client')
    competitions = relationship('Competition', back_populates='client')
    submissions = relationship('Submission', back_populates='client')

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        # TODO validate
        self._email = email

    def __repr__(self):
        return "<User(id='{}', username='{}')>".format(self.client_id, self.username)

    def to_dict(self):
        ret = {}
        for item in ("client_id", "username", "_email"):
            ret[item] = getattr(self, item)
        return ret


class APIKey(Base):
    __tablename__ = 'apikeys'
    apikey_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.client_id', ondelete='cascade'))
    client = relationship('Client', back_populates="apikeys")
    key = Column(String(100), nullable=False, default=lambda: secrets.token_urlsafe(TOKEN_WIDTH))
    secret = Column(String(100), nullable=False, default=lambda: secrets.token_urlsafe(TOKEN_WIDTH))

    @staticmethod
    def generateKey():
        return {"key": secrets.token_urlsafe(TOKEN_WIDTH),
                "secret": secrets.token_urlsafe(TOKEN_WIDTH)}

    def __repr__(self):
        return "<Key(id='{}', key='{}', secret='***')>".format(self.apikey_id, self.key)

    def to_dict(self):
        ret = {}
        for item in ("apikey_id", "client_id", "key", "secret"):
            ret[item] = getattr(self, item)
        return ret


class Competition(Base):
    __tablename__ = 'competitions'
    competition_id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    subtitle = Column(String(500), nullable=False)

    client_id = Column(Integer, ForeignKey('clients.client_id', ondelete='cascade'))
    client = relationship('Client', back_populates="competitions")

    type = Column(String(10), nullable=False)
    expiration = Column(DateTime, nullable=False)
    prize = Column(Integer, nullable=False)
    metric = Column(String(10), nullable=False)

    targets = Column(String(500), nullable=True)

    dataset = Column(JSON, nullable=True)
    dataset_url = Column(String(500), nullable=True)
    dataset_type = Column(String(10), nullable=True)

    dataset_kwargs = Column(JSON, nullable=True)
    dataset_key = Column(String(500), nullable=True)

    num_classes = Column(Integer, nullable=True)
    when = Column(DateTime, nullable=True)

    answer = Column(JSON, nullable=True)
    answer_url = Column(String(500), nullable=True)  # TODO
    answer_type = Column(String(10), nullable=True)
    answer_delay = Column(Integer, nullable=True)  # TODO

    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    submissions = relationship('Submission', back_populates='competition')

    def __repr__(self):
        return "<Competition(id='%s', clientId='%s')>" % (self.id, self.clientId)

    def to_dict(self):
        ret = {}
        for item in ("competition_id", "title", "client_id", "type", "expiration", "prize", "metric", "targets", "dataset",
                     "dataset_url", "dataset_type", "dataset_kwargs", "num_classes", "when", "answer", "answer_url", "answer_type",
                     "timestamp"):
            ret[item] = getattr(self, item)
        return ret

    @staticmethod
    def from_spec(client_id, spec):
        c = Competition(client_id=client_id,
                        title=spec.title,
                        subtitle=spec.subtitle,
                        expiration=spec.expiration + timedelta(seconds=spec.answer_delay),
                        type=spec.type.value,
                        prize=spec.prize,
                        metric=spec.metric.value,
                        dataset=spec.dataset if isinstance(spec.dataset, six.string_types) and validators.url(spec.dataset)
                        else spec.dataset.to_dict() if isinstance(spec.dataset, pd.DataFrame)
                        else '' if not spec.dataset else ujson.loads(spec.dataset),
                        dataset_type=spec.dataset_type.value,
                        dataset_kwargs=spec.dataset_kwargs,
                        dataset_key=spec.dataset_key,
                        num_classes=spec.num_classes,
                        targets=spec.targets if isinstance(spec.targets, six.string_types) else ujson.dumps(spec.targets),
                        when=spec.when,
                        answer=spec.answer if isinstance(spec.answer, six.string_types) and validators.url(spec.answer)
                        else spec.answer.to_dict() if isinstance(spec.answer, pd.DataFrame)
                        else '' if not spec.answer else ujson.loads(spec.answer),
                        answer_type=spec.dataset_type.value if spec.answer_type.value == "none" else spec.answer_type.value,
                        answer_delay=spec.answer_delay,
                        timestamp=datetime.now())
        return c


class Submission(Base):
    __tablename__ = 'submissions'
    submission_id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey('clients.client_id', ondelete='cascade'), nullable=False, )
    client = relationship(Client, back_populates='submissions')

    competition_id = Column(Integer, ForeignKey('competitions.competition_id', ondelete='cascade'), nullable=False, )
    competition = relationship('Competition', back_populates='submissions')

    score = Column(Integer)

    answer = Column(JSON, nullable=True)
    answer_url = Column(String(500), nullable=True)  # TODO
    answer_type = Column(String(10), nullable=True)

    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Submission(id='%s', clientId='%s', competitionId='%s')>" % (self.id, self.clientId, self.competitionId)

    def to_dict(self):
        ret = {}
        for item in ("submission_id", "client_id", "competition_id", "score", "answer", "answer_url", "answer_type", "timestamp"):
            ret[item] = getattr(self, item)
        return ret

    @staticmethod
    def from_spec(client_id, competition_id, competition, spec):
        c = Submission(client_id=client_id,
                       competition_id=competition_id,
                       score=-1,
                       competition=competition,
                       answer=spec.answer if isinstance(spec.answer, six.string_types) and validators.url(spec.answer)
                       else spec.answer.to_json() if isinstance(spec.answer, pd.DataFrame)
                       else '' if not spec.answer
                       else ujson.loads(spec.answer),
                       answer_type=spec.answer_type.value,
                       timestamp=datetime.now())
        return c
