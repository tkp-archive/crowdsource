import sys
import os.path
import tornado.ioloop
import tornado.web
from perspective import Table, PerspectiveManager, PerspectiveTornadoHandler
from .utils import log, parse_args
from .handlers import HTMLHandler, HTMLOpenHandler, LoginHandler, LogoutHandler, RegisterHandler, CompetitionHandler, SubmissionHandler, LeaderboardHandler


class ServerApplication(tornado.web.Application):
    def __init__(self, login, register, persist, basepath='/', wspath='ws:localhost:8080/', handlers=None, cookie_secret=None, proxies=None, debug=False):
        self._login = login
        self._register = register
        self._persist = persist

        self._clients = {}
        self._competitions = {}
        self._submissions = {}
        self._leaderboards = {}
        self._stash = []

        self._proxies = proxies
        self._basepath = basepath
        self._wspath = wspath

        self._manager = PerspectiveManager()
        self._table = Table([{"a": 1, "b": 2}])
        self._manager.host_table("data_source_one", self._table)

        root = os.path.join(os.path.dirname(__file__), 'assets')
        static = os.path.join(root, 'static')

        context = {'clients': self._clients,
                   'competitions': self._competitions,
                   'submissions': self._submissions,
                   'leaderboards': self._leaderboards,
                   'stash': self._stash,
                   'login': self._login,
                   'register': self._register,
                   'persist': self._persist,
                   'basepath': self._basepath,
                   'wspath': self._wspath,
                   'proxies': 'test'}

        default_handlers = [
            (r"/", HTMLOpenHandler, {'template': 'index.html', 'context': context}),
            (r"/index.html", HTMLOpenHandler, {'template': 'index.html', 'context': context, 'template_kwargs': {}}),
            (r"/home", HTMLOpenHandler, {'template': 'home.html',  'context': context}),
            (r"/login", HTMLOpenHandler, {'template': 'login.html',  'context': context}),
            (r"/register", HTMLOpenHandler, {'template': 'login.html',  'context': context}),
            (r"/logout", HTMLOpenHandler, {'template': 'logout.html',  'context': context}),
            (r"/competitions", HTMLHandler, {'template': 'competitions.html', 'template_kwargs': {'title': 'Competitions'},  'context': context}),
            (r"/submissions", HTMLHandler, {'template': 'submissions.html', 'template_kwargs': {'title': 'Submissions'},  'context': context}),
            (r"/leaderboard", HTMLHandler, {'template': 'leaderboard.html', 'template_kwargs': {'title': 'Leaderboard'},  'context': context}),
        ]

        default_handlers.extend([
            (r"/api/login", LoginHandler, context),
            (r"/api/logout", LogoutHandler, context),
            (r"/api/register", RegisterHandler, context),
            (r"/api/competition", CompetitionHandler, context),
            (r"/api/wscompetition", PerspectiveTornadoHandler, {"manager": self._manager, "check_origin": True}),
            (r"/api/submission", SubmissionHandler, context),
            (r"/api/leaderboard", LeaderboardHandler, context),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static}),
            (r"/(.*)", HTMLOpenHandler, {'template': '404.html', 'context': context})
        ])

        handlers = handlers or []
        for handler in handlers:
            for i, default in enumerate(default_handlers):
                if default[0] == handler[0]:
                    # override default handler
                    d = default[2]
                    d.update(handler[2])
                    default_handlers[i] = (handler[0], handler[1], d)

        settings = {
                "cookie_secret": cookie_secret or "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                "login_url": self._basepath + "login",
                "debug": debug,
                "template_path": os.path.join(root, 'templates'),
                }

        super(ServerApplication, self).__init__(default_handlers, **settings)


def main(*args, **kwargs):
    port = kwargs.get('port', 8080)

    if '-sql' in args:
        log.info('Using SQL auth')

        # defer sqlalchemy import
        from .login.sql import sqlalchemy_login
        from .persistence.sql import sqlalchemy_persist
        from .registration.sql import sqlalchemy_register

        login = sqlalchemy_login
        register = sqlalchemy_register
        persist = sqlalchemy_persist

    else:
        log.debug('Using null auth')
        from .login import null_login
        from .persistence import null_persist
        from .registration import null_register
        login = null_login
        register = null_register
        persist = null_persist

    application = ServerApplication(login, register, persist, debug='debug' in args)
    log.critical('LISTENING: %s', port)
    application.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    args, kwargs = parse_args(sys.argv)
    main(*args, **kwargs)
