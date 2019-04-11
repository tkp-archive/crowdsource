from ..structs import ClientStruct
from ..persistence.sql import Session
from ..persistence.models import Client


def sqlalchemy_login(handler, user):
    ret = Session().query(Client).filter_by(id=int(user)).first()
    if ret:
        return ClientStruct(id=str(ret.id))
    return None
