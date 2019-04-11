from crowdsource.samples import classify1, predict1, predict2, predictCorporateBonds, predictCitibike
from mock import patch, MagicMock


class TestClient:
    def test_all(self):
        with patch('crowdsource.samples.safe_post') as m, \
             patch('requests.get') as m2:
            m.return_value = '{}'
            m2.return_value = MagicMock()
            m2.return_value.json = MagicMock(return_value={'stationBeanList': [{'id': ''}]})

            assert classify1('http://test', 'test', None)
            assert predict1('http://test', 'test', None)
            assert predict2('http://test', 'test', None)
            assert predictCorporateBonds('http://test', 'test', None)
            assert predictCitibike('http://test', 'test', None)
