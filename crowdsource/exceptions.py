class MalformedCompetition(Exception):
    def __init__(self, *args, **kwargs):
        super(MalformedCompetition, self).__init__(
            "Malformed CompetitionType", *args, **kwargs
        )


class MalformedCompetitionSpec(Exception):
    def __init__(self, *args, **kwargs):
        super(MalformedCompetitionSpec, self).__init__(
            "Competition must be an instance of CompetitionSpec", *args, **kwargs
        )


class MalformedMetric(Exception):
    def __init__(self, *args, **kwargs):
        super(MalformedMetric, self).__init__(
            "Malformed DatasetFormat", *args, **kwargs
        )


class MalformedDataset(Exception):
    def __init__(self, *args, **kwargs):
        super(MalformedDataset, self).__init__(
            "Malformed DatasetFormat", *args, **kwargs
        )


class MalformedTargets(Exception):
    def __init__(self, *args, **kwargs):
        super(MalformedTargets, self).__init__(
            "Must provide targets for prediction competition", *args, **kwargs
        )


class MalformedDataType(Exception):
    def __init__(self, type, *args, **kwargs):
        super(MalformedDataType, self).__init__(
            "No handler for datatype - %s" % type, *args, **kwargs
        )
