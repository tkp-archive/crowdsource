from datetime import datetime, timedelta

import pandas as pd
import six
import ujson
import validators
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from tornado_sqlalchemy_login.sqla.models import (  # APIKey as APIKey,; noqa: F401
    Base,
    User,
)


class Client(User):
    __mapper_args__ = {"polymorphic_identity": "client"}

    competitions = relationship("Competition", back_populates="user")
    submissions = relationship("Submission", back_populates="user")


class Competition(Base):
    __tablename__ = "competitions"
    competition_id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    subtitle = Column(String(500), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"))
    user = relationship(Client, back_populates="competitions")

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

    submissions = relationship("Submission", back_populates="competition")

    def __repr__(self):
        return "<Competition(id='%s', userId='%s')>" % (self.id, self.userId)

    def to_dict(self, private=False):
        ret = {}
        for item in (
            "competition_id",
            "title",
            "user_id",
            "type",
            "expiration",
            "prize",
            "metric",
            "targets",
            "dataset",
            "dataset_url",
            "dataset_type",
            "dataset_kwargs",
            "num_classes",
            "when",
            "timestamp",
        ):
            ret[item] = getattr(self, item)
        if private:
            for item in (
                "answer",
                "answer_url",
                "answer_type",
            ):
                ret[item] = getattr(self, item)
        return ret

    @staticmethod
    def from_spec(user_id, spec):
        c = Competition(
            user_id=user_id,
            title=spec.title,
            subtitle=spec.subtitle,
            expiration=spec.expiration + timedelta(seconds=spec.answer_delay),
            type=spec.type.value,
            prize=spec.prize,
            metric=spec.metric.value,
            dataset=spec.dataset
            if isinstance(spec.dataset, six.string_types)
            and validators.url(spec.dataset)
            else spec.dataset.to_dict()
            if isinstance(spec.dataset, pd.DataFrame)
            else ""
            if not spec.dataset
            else ujson.loads(spec.dataset),
            dataset_type=spec.dataset_type.value,
            dataset_kwargs=spec.dataset_kwargs,
            dataset_key=spec.dataset_key,
            num_classes=spec.num_classes,
            targets=spec.targets
            if isinstance(spec.targets, six.string_types)
            else ujson.dumps(spec.targets),
            when=spec.when,
            answer=spec.answer
            if isinstance(spec.answer, six.string_types) and validators.url(spec.answer)
            else spec.answer.to_dict()
            if isinstance(spec.answer, pd.DataFrame)
            else ""
            if not spec.answer
            else ujson.loads(spec.answer),
            answer_type=spec.dataset_type.value
            if spec.answer_type.value == "none"
            else spec.answer_type.value,
            answer_delay=spec.answer_delay,
            timestamp=datetime.now(),
        )
        return c


class Submission(Base):
    __tablename__ = "submissions"
    submission_id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )
    user = relationship(Client, back_populates="submissions")

    competition_id = Column(
        Integer,
        ForeignKey("competitions.competition_id", ondelete="cascade"),
        nullable=False,
    )
    competition = relationship(Competition, back_populates="submissions")

    score = Column(Integer)

    answer = Column(JSON, nullable=True)
    answer_url = Column(String(500), nullable=True)  # TODO
    answer_type = Column(String(10), nullable=True)

    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Submission(id='%s', userId='%s', competitionId='%s')>" % (
            self.id,
            self.userId,
            self.competitionId,
        )

    def to_dict(self, private=False):
        ret = {}
        for item in (
            "submission_id",
            "user_id",
            "competition_id",
            "score",
            "timestamp",
        ):
            ret[item] = getattr(self, item)
        if private:
            for item in (
                "answer",
                "answer_url",
                "answer_type",
            ):
                ret[item] = getattr(self, item)
        return ret

    @staticmethod
    def from_spec(user_id, competition_id, competition, spec):
        c = Submission(
            user_id=user_id,
            competition_id=competition_id,
            score=-1,
            competition=competition,
            answer=spec.answer
            if isinstance(spec.answer, six.string_types) and validators.url(spec.answer)
            else spec.answer.to_json()
            if isinstance(spec.answer, pd.DataFrame)
            else ""
            if not spec.answer
            else ujson.loads(spec.answer),
            answer_type=spec.answer_type.value,
            timestamp=datetime.now(),
        )
        return c
