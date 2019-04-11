from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .utils import competition_struct_to_sql, submission_struct_to_sql
from ..structs import ClientStruct, CompetitionStruct, SubmissionStruct
from ..utils import log

SQLDB = create_engine('postgresql://cs:crowdsource@localhost:8890/')  # TODO
Session = sessionmaker(bind=SQLDB)


def add_and_commit(thing):
    session = Session()
    session.add(thing)
    session.commit()
    return thing.id


def sqlalchemy_persist(handler, struct, update=False, *args, **kwargs):
    if isinstance(struct, ClientStruct):
        log.info('Persisting client %d', struct.id)
        pass
    elif isinstance(struct, CompetitionStruct):
        log.info('Persisting competition %d', struct.id)
        c = competition_struct_to_sql(struct)
        struct.id = add_and_commit(c)

    elif isinstance(struct, SubmissionStruct):
        log.debug('Persisting submission %d', struct.id)
        s = submission_struct_to_sql(struct)
        struct.id = add_and_commit(s)

    else:
        log.info('Cannot persist type %s', type(struct))
