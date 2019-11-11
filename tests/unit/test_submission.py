from crowdsource.types.submission import SubmissionSpec


class TestSubmissionSpec:
    def test_init(self):
        SubmissionSpec(competition_id=2,
                       answer='[{"id":3}]',
                       answer_type='none')

    def test_to_dict_from_dict(self):
        s = SubmissionSpec(competition_id=2,
                           answer='[{"id":3}]',
                           answer_type='none')

        d = s.to_dict()
        j = s.to_json()

        s2 = SubmissionSpec.from_dict(d)
        s3 = SubmissionSpec.from_json(j)

        for item in ['competition_id', 'answer_type']:
            assert getattr(s, item) == getattr(s2, item) == getattr(s3, item)
