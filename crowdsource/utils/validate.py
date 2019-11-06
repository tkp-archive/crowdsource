from .utils import parse_body, log
from .enums import CompetitionType
from .utils import _CLIENT_NO_ID, _CLIENT_NOT_REGISTERED, _COMPETITION_NO_ID, _COMPETITION_NOT_REGISTERED, _NO_SUBMISSION, _COMPETITION_MALFORMED, _SUBMISSION_MALFORMED, str_or_unicode


def validate_competition_get(handler):
    data = parse_body(handler.request)

    data['id'] = data.get('id', handler.get_argument('id', ()))
    data['client_id'] = data.get('client_id', handler.get_argument('client_id', ()))
    data['type'] = data.get('type', handler.get_argument('type', ()))

    if str_or_unicode(data['id']):
        data['id'] = str(data['id']).split(',')

    if str_or_unicode(data['client_id']):
        data['client_id'] = str(data['client_id']).split(',')

    if str_or_unicode(data['type']):
        data['type'] = list(map(lambda x: CompetitionType(x), str(data['type']).split(',')))

    log.info("GET COMPETITIONS")
    return data


def validate_competition_post(handler):
    data = parse_body(handler.request)
    if not data.get('id'):
        handler._set_401(_CLIENT_NO_ID)

    if data.get('id', '') not in handler._clients:
        handler._set_401(_CLIENT_NOT_REGISTERED)

    if data.get('spec', None) is None:
        handler._set_400(_COMPETITION_MALFORMED)
    return data


def validate_submission_get(handler):
    data = parse_body(handler.request)

    data['id'] = data.get('id', handler.get_argument('id', ()))
    data['client_id'] = data.get('client_id', handler.get_argument('client_id', ()))
    data['competition_id'] = data.get('competition_id', handler.get_argument('competition_id', ()))
    data['type'] = data.get('type', handler.get_argument('type', ()))

    if str_or_unicode(data['id']):
        data['id'] = str(data['id']).split(',')

    if str_or_unicode(data['client_id']):
        data['client_id'] = str(data['client_id']).split(',')

    if str_or_unicode(data['competition_id']):
        data['competition_id'] = str(data['competition_id']).split(',')

    if str_or_unicode(data['type']):
        data['type'] = list(map(lambda x: CompetitionType(x), str(data['type']).split(',')))

    log.info("GET SUBMISSIONS")
    return data


def validate_submission_post(handler):
    data = parse_body(handler.request)

    if not data.get('id'):
        handler._set_401(_CLIENT_NO_ID)

    if data.get('id') not in handler._clients:
        handler._set_401(_CLIENT_NOT_REGISTERED)

    if not data.get('competition_id'):
        handler._set_401(_COMPETITION_NO_ID)

    if data.get('competition_id') not in handler._competitions:
        handler._set_401(_COMPETITION_NOT_REGISTERED)

    if not data.get('submission'):
        handler._set_400(_NO_SUBMISSION)

    log.info("POST SUBMISSION %s", data.get('id'))
    return data


def validate_leaderboard_get(handler):
    data = parse_body(handler.request)

    data['id'] = data.get('id', handler.get_argument('id', ()))
    data['client_id'] = data.get('client_id', handler.get_argument('client_id', ()))
    data['competition_id'] = data.get('competition_id', handler.get_argument('competition_id', ()))
    data['type'] = data.get('type', handler.get_argument('type', ()))

    if str_or_unicode(data['id']):
        data['id'] = str(data['id']).split(',')

    if str_or_unicode(data['client_id']):
        data['client_id'] = str(data['client_id']).split(',')

    if str_or_unicode(data['competition_id']):
        data['competition_id'] = str(data['competition_id']).split(',')

    if str_or_unicode(data['type']):
        data['type'] = list(map(lambda x: CompetitionType(x), str(data['type']).split(',')))

    log.info("GET SUBMISSIONS")
    return data
