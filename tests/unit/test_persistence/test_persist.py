import pandas
from datetime import datetime, timedelta
from mock import MagicMock
from crowdsource.structs import ClientStruct, CompetitionStruct, SubmissionStruct
from crowdsource.persistence import null_persist
from sklearn.datasets import make_classification
from crowdsource.competition import CompetitionSpec
from crowdsource.submission import SubmissionSpec
from crowdsource.utils.enums import CompetitionType, CompetitionMetric, DatasetFormat


class TestPersist:
    def test_null_persistclient(self):
        null_persist(MagicMock(), ClientStruct(1))

    def test_null_persistcompetition(self):
        dataset = make_classification()
        s = CompetitionSpec(title='',
                            type=CompetitionType.CLASSIFY,
                            expiration=datetime.now() + timedelta(minutes=1),
                            prize=1.0,
                            num_classes=2,
                            dataset=pandas.DataFrame(dataset[0]),
                            metric=CompetitionMetric.LOGLOSS,
                            answer=pandas.DataFrame(dataset[1]))
        null_persist(MagicMock(), CompetitionStruct(1, 2, s.to_dict()))

    def test_null_persistsubmission(self):
        dataset = make_classification()
        s = CompetitionSpec(title='',
                            type=CompetitionType.CLASSIFY,
                            expiration=datetime.now() + timedelta(minutes=1),
                            prize=1.0,
                            num_classes=2,
                            dataset=pandas.DataFrame(dataset[0]),
                            metric=CompetitionMetric.LOGLOSS,
                            answer=pandas.DataFrame(dataset[1]))
        c = CompetitionStruct(1, 2, s.to_dict())

        ss = SubmissionSpec(1, 'http://test.com', DatasetFormat.JSON)
        null_persist(MagicMock(), SubmissionStruct(1, 2, 3, c, ss.to_dict(), 5.0))
