import logging
import six
from ..utils import parse_body
from ..enums import CompetitionType
from ..persistence.models import Competition
from ..utils import _CLIENT_NO_ID, _CLIENT_NOT_REGISTERED, _COMPETITION_NO_ID, _COMPETITION_NOT_REGISTERED, _NO_SUBMISSION, _COMPETITION_MALFORMED


def validate_competition_get(handler):
    data = parse_body(handler.request)

    data['competition_id'] = data.get('competition_id', handler.get_argument('competition_id', ()))
    data['client_id'] = data.get('client_id', handler.get_argument('client_id', ()))
    data['type'] = data.get('type', handler.get_argument('type', ()))

    if isinstance(data['competition_id'], six.string_types):
        data['competition_id'] = str(data['competition_id']).split(',')

    if isinstance(data['client_id'], six.string_types):
        data['client_id'] = str(data['client_id']).split(',')

    if isinstance(data['type'], six.string_types):
        data['type'] = list(map(lambda x: CompetitionType(x), str(data['type']).split(',')))

    logging.info("GET COMPETITIONS")
    return data


def validate_competition_post(handler):
    data = parse_body(handler.request)
    if not data.get('competition_id'):
        handler._set_401(_CLIENT_NO_ID)

    if int(data.get('competition_id', '-1')) not in handler._clients:
        handler._set_401(_CLIENT_NOT_REGISTERED)

    if data.get('spec', None) is None:
        handler._set_400(_COMPETITION_MALFORMED)
    return data


def validate_submission_get(handler):
    data = parse_body(handler.request)

    data['submission_id'] = data.get('id', handler.get_argument('submission_id', ()))
    data['client_id'] = data.get('client_id', handler.get_argument('client_id', ()))
    data['competition_id'] = data.get('competition_id', handler.get_argument('competition_id', ()))
    data['type'] = data.get('type', handler.get_argument('type', ()))

    if isinstance(data['submission_id'], six.string_types):
        data['submission_id'] = str(data['submission_id']).split(',')

    if isinstance(data['client_id'], six.string_types):
        data['client_id'] = str(data['client_id']).split(',')

    if isinstance(data['competition_id'], six.string_types):
        data['competition_id'] = str(data['competition_id']).split(',')

    if isinstance(data['type'], six.string_types):
        data['type'] = list(map(lambda x: CompetitionType(x), str(data['type']).split(',')))

    logging.info("GET SUBMISSIONS")
    return data


def validate_submission_post(handler):
    data = parse_body(handler.request)

    if not data.get('client_id'):
        handler._set_401(_CLIENT_NO_ID)

    if int(data.get('client_id', '-1')) not in handler._clients:
        handler._set_401(_CLIENT_NOT_REGISTERED)

    if not data.get('competition_id'):
        handler._set_401(_COMPETITION_NO_ID)

    with handler.session() as session:
        competition = session.query(Competition).filter_by(competition_id=int(data.get('competition_id'))).first()
        if competition is None:
            handler._set_401(_COMPETITION_NOT_REGISTERED)

    if not data.get('submission'):
        handler._set_400(_NO_SUBMISSION)

    logging.info("POST SUBMISSION %s", data.get('submission_id'))
    return data


def validate_leaderboard_get(handler):
    data = parse_body(handler.request)

    data['submission_id'] = data.get('submission_id', handler.get_argument('submission_id', ()))
    data['client_id'] = data.get('client_id', handler.get_argument('client_id', ()))
    data['competition_id'] = data.get('competition_id', handler.get_argument('competition_id', ()))
    data['type'] = data.get('type', handler.get_argument('type', ()))

    if isinstance(data['submission_id'], six.string_types):
        data['submission_id'] = str(data['submission_id']).split(',')

    if isinstance(data['client_id'], six.string_types):
        data['client_id'] = str(data['client_id']).split(',')

    if isinstance(data['competition_id'], six.string_types):
        data['competition_id'] = str(data['competition_id']).split(',')

    if isinstance(data['type'], six.string_types):
        data['type'] = list(map(lambda x: CompetitionType(x), str(data['type']).split(',')))

    logging.info("GET SUBMISSIONS")
    return data
