import tornado.web
import ujson
from .base import ServerHandler
from ..utils.utils import _REGISTER, _CLIENT_MALFORMED
from ..utils.validate import validate_register_get, validate_register_post


class RegisterHandler(ServerHandler):
    @tornado.web.authenticated
    def get(self):
        '''Get the current list of client ids'''
        data = self._validate(validate_register_get)

        if self.current_user and self.current_user.decode('utf-8') not in self._clients:
            return self.post()

        # paginate
        page = int(data.get('page', 0))
        self.write(ujson.dumps([c.to_dict() for c in list(self._clients.values())[page*100:(page+1)*100]]))

    def post(self):
        '''Register a client. Client will be assigned a session id'''
        data = self._validate(validate_register_post)
        ret = self._register_or_known(data)
        if ret:
                self._writeout(ujson.dumps(ret), _REGISTER, ret['id'])
        else:
            self._set_403(_CLIENT_MALFORMED)
