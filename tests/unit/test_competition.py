import pandas
from datetime import datetime, timedelta
from sklearn.datasets import make_classification
from crowdsource.types.competition import CompetitionSpec
from crowdsource.enums import CompetitionType, CompetitionMetric


class TestCompetitionSpec:
    def test_init(self):
        dataset = make_classification()
        CompetitionSpec(title='',
                        type=CompetitionType.CLASSIFY,
                        expiration=datetime.now() + timedelta(minutes=1),
                        prize=1.0,
                        num_classes=2,
                        dataset=pandas.DataFrame(dataset[0]),
                        metric=CompetitionMetric.LOGLOSS,
                        answer=pandas.DataFrame(dataset[1]))

    def test_to_dict_from_dict(self):
        time = datetime(2018, 1, 1)
        s = CompetitionSpec(title='',
                            type=CompetitionType.CLASSIFY,
                            expiration=time,
                            prize=1.0,
                            num_classes=2,
                            dataset='http://test.com',
                            metric=CompetitionMetric.LOGLOSS,
                            answer='http://test.com')

        print(str(s))
        d = s.to_dict()

        d['expiration'] = time.strftime("%Y-%m-%d %H:%M:%S")

        j = s.to_json()

        s2 = CompetitionSpec.from_dict(d)
        s3 = CompetitionSpec.from_json(j)

        for item in ['type', 'expiration', 'prize', 'num_classes', 'metric']:
            assert getattr(s, item) == getattr(s2, item) == getattr(s3, item)
