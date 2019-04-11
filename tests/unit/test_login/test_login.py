from mock import MagicMock
from crowdsource.login import null_login


class TestLogin:
    def test_null_login(self):
        null_login(MagicMock(), -1)
