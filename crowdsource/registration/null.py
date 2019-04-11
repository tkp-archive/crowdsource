from ..utils.utils import _genrand
from ..structs import ClientStruct


def null_register(handler, data):
    '''
    handler: instance of crowdsource.handlers.ServerHandler
    data: dictionary containing registration information
    returns: crowdsource.Structs.ClientStruct
    '''
    ids = [c.id for c in handler._clients.values()]
    id = str(_genrand(ids))
    return ClientStruct(id=id)
