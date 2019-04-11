from crowdsource.utils.exceptions import MalformedCompetition, MalformedCompetitionSpec, MalformedMetric, MalformedDataset, MalformedTargets, MalformedDataType


class TestException:
    def test_all(self):
        MalformedCompetition()
        MalformedCompetitionSpec()
        MalformedMetric()
        MalformedDataset()
        MalformedTargets()
        MalformedDataType(int)
