from crowdsource.structs import ClientStruct, CompetitionStruct, SubmissionStruct
from mock import patch, MagicMock
import pandas
from datetime import datetime, timedelta
from sklearn.datasets import make_classification
from crowdsource.types.competition import CompetitionSpec
from crowdsource.enums import CompetitionType, CompetitionMetric


dataset = make_classification()
competition = CompetitionSpec(title='',
                              type=CompetitionType.CLASSIFY,
                              expiration=datetime.now() + timedelta(minutes=1),
                              prize=1.0,
                              num_classes=2,
                              dataset=pandas.DataFrame(dataset[0]),
                              metric=CompetitionMetric.LOGLOSS,
                              answer=pandas.DataFrame(dataset[1]))


class TestStructs:
    def test_init(self):
        c = ClientStruct(1)

        d = competition.to_dict()

        c2 = CompetitionStruct(1, 2, d)

        d2 = {'competitionId': 2, 'answer': '[{"id":3}]', 'answer_type': 'none'}
        s = SubmissionStruct(1, 2, 3, c2, d2, 1)

    def test_to_dict(self):
        d = competition.to_dict()
        c2 = CompetitionStruct(1, 2, d)
        d2 = {'competitionId': 2, 'answer': '[{"id":3}]', 'answer_type': 'none'}
        s = SubmissionStruct(1, 2, 3, c2, d2, 1)

        c2.to_dict()
        c2.to_json()

        s.to_dict()
        s.to_json()
