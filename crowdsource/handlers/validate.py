import logging
import six
from tornado_sqlalchemy_login.utils import parse_body
from ..enums import CompetitionType
from ..persistence.models import Competition


def validate_competition_get(handler):
    data = parse_body(handler.request)

    data['competition_id'] = data.get('competition_id', handler.get_argument('competition_id', ()))
    data['user_id'] = data.get('user_id', handler.get_argument('user_id', ()))
    data['type'] = data.get('type', handler.get_argument('type', ()))

    if isinstance(data['competition_id'], six.string_types):
        data['competition_id'] = str(data['competition_id']).split(',')

    if isinstance(data['user_id'], six.string_types):
        data['user_id'] = str(data['user_id']).split(',')

    if isinstance(data['type'], six.string_types):
        data['type'] = list(map(lambda x: CompetitionType(x), str(data['type']).split(',')))

    logging.info("GET COMPETITIONS")
    return data


def validate_competition_post(handler):
    data = parse_body(handler.request)
    if not handler.get_current_user() or int(handler.get_current_user()) not in handler._users:
        handler._set_401('User no id')

    if data.get('spec', None) is None:
        handler._set_400('Competition malformed')
    return data


def validate_submission_get(handler):
    data = parse_body(handler.request)

    data['submission_id'] = data.get('id', handler.get_argument('submission_id', ()))
    data['user_id'] = data.get('user_id', handler.get_argument('user_id', ()))
    data['competition_id'] = data.get('competition_id', handler.get_argument('competition_id', ()))
    data['type'] = data.get('type', handler.get_argument('type', ()))

    if isinstance(data['submission_id'], six.string_types):
        data['submission_id'] = str(data['submission_id']).split(',')

    if isinstance(data['user_id'], six.string_types):
        data['user_id'] = str(data['user_id']).split(',')

    if isinstance(data['competition_id'], six.string_types):
        data['competition_id'] = str(data['competition_id']).split(',')

    if isinstance(data['type'], six.string_types):
        data['type'] = list(map(lambda x: CompetitionType(x), str(data['type']).split(',')))

    logging.info("GET SUBMISSIONS")
    return data


def validate_submission_post(handler):
    data = parse_body(handler.request)

    if not handler.get_current_user() or int(handler.get_current_user()) not in handler._users:
        handler._set_401('User no id')

    if not data.get('competition_id'):
        handler._set_400('Competition no id')

    with handler.session() as session:
        competition = session.query(Competition).filter_by(competition_id=int(data.get('competition_id'))).first()
        if competition is None:
            handler._set_400('Competition not registered')

    if not data.get('submission'):
        handler._set_400('User provided no submission')

    logging.info("POST SUBMISSION %s", data.get('submission_id'))
    return data


def validate_leaderboard_get(handler):
    data = parse_body(handler.request)

    data['submission_id'] = data.get('submission_id', handler.get_argument('submission_id', ()))
    data['user_id'] = data.get('user_id', handler.get_argument('user_id', ()))
    data['competition_id'] = data.get('competition_id', handler.get_argument('competition_id', ()))
    data['type'] = data.get('type', handler.get_argument('type', ()))

    if isinstance(data['submission_id'], six.string_types):
        data['submission_id'] = str(data['submission_id']).split(',')

    if isinstance(data['user_id'], six.string_types):
        data['user_id'] = str(data['user_id']).split(',')

    if isinstance(data['competition_id'], six.string_types):
        data['competition_id'] = str(data['competition_id']).split(',')

    if isinstance(data['type'], six.string_types):
        data['type'] = list(map(lambda x: CompetitionType(x), str(data['type']).split(',')))

    logging.info("GET SUBMISSIONS")
    return data
