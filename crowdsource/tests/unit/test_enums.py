from crowdsource.enums import (
    DatasetType,
    DatasetFormat,
    CompetitionType,
    CompetitionMetric,
)


class TestEnums:
    def test_all(self):
        assert DatasetType.NONE.value == "none"
        assert DatasetType.PROVIDED.value == "provided"
        assert DatasetType.REMOTE.value == "remote"
        assert DatasetFormat.NONE.value == "none"
        assert DatasetFormat.JSON.value == "json"
        assert DatasetFormat.CSV.value == "csv"
        assert CompetitionType.PREDICT.value == "predict"
        assert CompetitionType.CLASSIFY.value == "classify"
        assert CompetitionType.CLUSTER.value == "cluster"
        assert CompetitionMetric.LOGLOSS.value == "logloss"
        assert CompetitionMetric.ABSDIFF.value == "absdiff"
