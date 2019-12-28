import copy
from tornado_sqlalchemy_login.handlers import BaseHandler as _BaseHandler, AuthenticatedHandler


class BaseHandler(_BaseHandler):
    def initialize(self, **kwargs):
        for attr in ('clients', 'all_clients', 'competitions', 'all_competitions', 'submissions', 'all_submissions', 'leaderboards', 'stash', 'proxies'):
            setattr(self, '_{}'.format(attr), kwargs.pop(attr, ''))
        super(BaseHandler, self).initialize(**kwargs)


class HTMLHandler(BaseHandler):
    def initialize(self, template=None, basepath="/", wspath="/", **kwargs):
        super(HTMLHandler, self).initialize(template=template, basepath=basepath, wspath=wspath)

    def get(self):
        '''Get the login page'''
        template = self.render_template(self.template)
        self.write(template)
