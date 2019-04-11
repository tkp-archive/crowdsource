from crowdsource.utils.validate import validate_login_get, validate_login_post
from mock import MagicMock, patch


class TestValidate:
    def test_all(self):
        with patch('crowdsource.utils.validate.log'), \
             patch('crowdsource.utils.validate.parse_body'):
            validate_login_get(None)
            validate_login_post(MagicMock())
