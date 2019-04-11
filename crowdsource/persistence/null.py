from ..utils import _genrand
from ..structs import ClientStruct, CompetitionStruct, SubmissionStruct


def null_persist(handler, struct, update=False, *args, **kwargs):
    '''
    handler: instance of crowdsource.handlers.ServerHandler
    struct: an instance of crowdsource.Structs.{ClientStruct, CompetitionStruct, SubmissionStruct}
    returns: None
    '''
    if isinstance(struct, ClientStruct):
        pass

    elif isinstance(struct, CompetitionStruct):
        ids = [c.id for c in handler._competitions.values()]
        id = str(_genrand(ids))
        struct.id = id

    elif isinstance(struct, SubmissionStruct):
        ids = [s.id for c in handler._submissions.values() for s in c]
        id = str(_genrand(ids))
        struct.id = id
