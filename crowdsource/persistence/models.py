from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)

    competitions = relationship('Competition', back_populates='client')
    submissions = relationship('Submission', back_populates='client')

    def __repr__(self):
        return "<User(id='%s')>" % self.id


class Competition(Base):
    __tablename__ = 'competitions'
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)

    clientId = Column(Integer, ForeignKey('clients.id', ondelete='cascade'))
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
        for item in ("id", "title", "clientId", "type", "expiration", "prize", "metric", "targets", "dataset",
                     "dataset_url", "dataset_type", "num_classes", "when", "answer", "answer_url", "answer_type",
                     "timestamp"):
            ret[item] = getattr(self, item)
        return ret


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)

    clientId = Column(Integer, ForeignKey('clients.id', ondelete='cascade'), nullable=False, )
    client = relationship(Client, back_populates='submissions')

    competitionId = Column(Integer, ForeignKey('competitions.id', ondelete='cascade'), nullable=False, )
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
        for item in ("id", "clientId", "competitionId", "score", "answer", "answer_url", "answer_type", "timestamp"):
            ret[item] = getattr(self, item)
        return ret
