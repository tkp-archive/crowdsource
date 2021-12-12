from enum import Enum


class DatasetType(Enum):
    NONE = "none"
    PROVIDED = "provided"
    REMOTE = "remote"


class DatasetFormat(Enum):
    NONE = "none"
    CSV = "csv"
    JSON = "json"


class CompetitionType(Enum):
    """Enumeration of possible competitions"""

    PREDICT = "predict"
    CLASSIFY = "classify"
    CLUSTER = "cluster"


class CompetitionMetric(Enum):
    """Enumeration of competition metrics"""

    LOGLOSS = "logloss"
    ABSDIFF = "absdiff"


class AnswerType(Enum):
    """Enumeration of the answer forms"""

    ONE = 1  # Classify
    TWO = 2  # Predict 1
    THREE = 3  # Predict 2
    FOUR = 4  # Predict 3
    FIVE = 5  # Predict 4
    SIX = 6  # Predict 5
    SEVEN = 7  # Predict 6
    EIGHT = 8  # Predict 7
    NINE = 9  # Predict 8
    TEN = 10  # Cluster
