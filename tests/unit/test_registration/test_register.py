from mock import MagicMock
from crowdsource.registration import null_register
from crowdsource.structs import ClientStruct


class TestRegister:
    def test_null_register(self):
        null_register(MagicMock(), ClientStruct(1))
