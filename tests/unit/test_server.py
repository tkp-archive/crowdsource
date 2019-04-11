from crowdsource.server import ServerApplication, main
from crowdsource.login import null_login
from crowdsource.persistence import null_persist
from crowdsource.registration import null_register
from mock import patch


class TestServer:
    def test_init(self):
        ServerApplication(null_login, null_persist, null_register, handlers=[])

    def test_main(self):
        with patch('tornado.ioloop.IOLoop.current'), patch('tornado.web.Application.listen'), patch('crowdsource.server.ServerApplication'):
            main()

        with patch('tornado.ioloop.IOLoop.current'), patch('tornado.web.Application.listen'), patch('crowdsource.server.ServerApplication'):
            main('sql')
