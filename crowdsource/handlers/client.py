import tornado.web
import ujson
from .base import ServerHandler
from ..persistence.models import Client
from ..structs import ClientStruct
from ..utils.utils import _REGISTER, _CLIENT_MALFORMED


class RegisterHandler(ServerHandler):
    @tornado.web.authenticated
    def get(self):
        '''Get the current list of client ids'''
        if self.current_user and self.current_user.decode('utf-8') not in self._clients:
            return self.post()

        # paginate
        page = int(self.get_argument('page', 0))
        self.write(ujson.dumps([c.to_dict() for c in list(self._clients.values())[page*100:(page+1)*100]]))

    def post(self):
        '''Register a client. Client will be assigned a session id'''
        with self.session() as session:
            c = Client()
            session.add(c)
            session.commit()
            session.refresh(c)
            ret = self._login_post(ClientStruct(str(c.id)))

        if ret:
            self._writeout(ujson.dumps(ret), _REGISTER, ret["id"])
        else:
            self._set_403(_CLIENT_MALFORMED)
