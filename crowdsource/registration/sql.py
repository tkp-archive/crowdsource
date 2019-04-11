from ..persistence.models import Client
from ..persistence.sql import add_and_commit
from ..structs import ClientStruct


def sqlalchemy_register(handler, data):
    c = Client()
    id = add_and_commit(c)
    return ClientStruct(str(id))
