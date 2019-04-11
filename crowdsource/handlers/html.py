import tornado.web
import copy
from .base import ServerHandler
from ..utils.validate import validate_login_post, validate_register_post


def get_kwargs(handler, template_kwargs):
    kwargs = copy.deepcopy(template_kwargs)
    for k in kwargs:
        if callable(kwargs[k]):
            kwargs[k] = kwargs[k](handler)
    return kwargs


class HTMLOpenHandler(ServerHandler):
    def initialize(self, context=None, template=None, template_kwargs=None, **kwargs):
        super(HTMLOpenHandler, self).initialize(**context)
        self.template = template
        self.template_kwargs = template_kwargs or {}

    def get(self, *args):
        '''Get the login page'''
        if not self.template:
            self.redirect(self.basepath)
        else:
            if 'logout' in self.request.path:
                self.clear_cookie("user")

            # TODO hack
            kwargs = get_kwargs(self, self.template_kwargs)
            # endhack

            template = self.render_template(self.template, **kwargs)
            self.write(template)

    def post(self, *args):
        if 'login' in self.request.path:
            self._validate(validate_login_post)
            user = self.get_argument('id', '') or self.current_user.decode('utf-8') or ''
            client = self._login(user)
            ret = self._login_post(client)
            if not ret:
                self.redirect(self.basepath + 'login')
                return

        elif 'register' in self.request.path:
            data = self._validate(validate_register_post)
            ret = self._register_or_known(data)
            if not ret:
                self.redirect(self.basepath + 'login')
                return
        self.redirect(self.get_argument('next', self.basepath))


class HTMLHandler(HTMLOpenHandler):
    @tornado.web.authenticated
    def get(self, *args):
        '''Get the login page'''
        if not self.template:
            self.redirect('')
        else:
            # TODO hack
            kwargs = get_kwargs(self, self.template_kwargs)
            # endhack

            template = self.render_template(self.template, **kwargs)
            self.write(template)
