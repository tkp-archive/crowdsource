import pandas
import validators
from .models import Client, Competition, Submission


def client_struct_to_sql(client):
    return Client(id=client.id)


def competition_struct_to_sql(competition):
    c = Competition()
    c.clientId = competition.clientId
    # client = relationship('Client', back_populates="competitions")

    c.type = competition.type.value
    c.expiration = competition.expiration
    c.prize = competition.prize
    c.metric = competition.metric.value
    c.targets = competition.targets

    if isinstance(competition.dataset, pandas.DataFrame):
        c.dataset = competition.dataset.to_json()
    elif validators.url(competition.dataset):
        c.dataset_url = competition.dataset
    else:
        raise Exception()  # TODO

    c.dataset_type = competition.dataset_type.value
    c.dataset_kwargs = competition.dataset_kwargs
    c.dataset_key = competition.dataset_key

    c.num_classes = competition.num_classes
    c.when = competition.when

    if isinstance(competition.answer, pandas.DataFrame):
        c.answer = competition.answer.to_json()
    elif validators.url(competition.answer):
        c.answer_url = competition.answer  # TODO
    else:
        raise Exception()  # TODO

    c.answer_type = competition.answer_type.value

    # c.answer_delay = 0 # TODO competition.answer_delay

    # timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    # submissions = relationship('Submission', back_populates='competition')
    return c


def submission_struct_to_sql(submission):
    s = Submission()
    s.clientId = submission.clientId
    # client = relationship(Client, back_populates='submissions')

    s.competitionId = submission.competitionId
    # competition = relationship('Competition', back_populates='submissions')

    s.score = submission.score
    if isinstance(submission.answer, pandas.DataFrame):
        s.answer = submission.answer.to_json()
    elif validators.url(submission.answer):
        s.answer_url = submission.answer_url
    else:
        raise Exception()  # TODO

    s.answer_type = submission.answer_type

    # timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    return s
