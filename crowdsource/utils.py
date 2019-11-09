try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
    ConnectionRefusedError = OSError
import logging
import random
import requests
import tornado
import ujson

_SKIP_REREGISTER = 'Skipping re-registration for client %s'
_REGISTER = 'Registering client %s'
_REGISTER_COMPETITION = 'Registering competition %s from %s'
_REGISTER_SUBMISSION = 'New Submission %s from %s'
_FORBIDDEN = 'Forbidden'
_CLIENT_NO_ID = 'Client did not provide id'
_CLIENT_NOT_REGISTERED = 'Client not registered'
_CLIENT_MALFORMED = 'Client Malformed'
_COMPETITION_NO_ID = 'Client did not provide competition id'
_COMPETITION_NOT_REGISTERED = 'Competition not registered/active'
_COMPETITION_MALFORMED = 'Client provided malformed competition'
_NO_SUBMISSION = 'Client provided no submission'
_SUBMISSION_MALFORMED = 'Client provided malformed submission'


def parse_body(req, **fields):
    try:
        data = tornado.escape.json_decode(req.body)
    except ValueError:
        data = {}
    return data


def _genrand(values, x=10000):
    id = random.randint(0, x)
    while id in values:
        id = random.randint(0, x)
    return id


def safe_get(path, data=None, cookies=None, proxies=None):
    try:
        resp = requests.get(path, data=data, cookies=cookies, proxies=proxies)
        return ujson.loads(resp.text)
    except ConnectionRefusedError:
        return {}
    except ValueError:
        logging.critical("route:{}\terror code: {}\t{}".format(path, resp.status_code, resp.text))
        raise


def safe_post(path, data=None, cookies=None, proxies=None):
    try:
        resp = requests.post(path, data=data, cookies=cookies, proxies=proxies)
        return ujson.loads(resp.text)
    except ConnectionRefusedError:
        return {}
    except ValueError:
        logging.critical("route:{}\nerror code: {}\t{}".format(path, resp.status_code, resp.text))
        raise


def safe_post_cookies(path, data=None, cookies=None, proxies=None):
    try:
        resp = requests.post(path, data=data, cookies=cookies, proxies=proxies)
        return ujson.loads(resp.text), resp.cookies
    except ConnectionRefusedError:
        return {}, None
    except ValueError:
        logging.critical("route:{}\nerror code: {}\t{}".format(path, resp.status_code, resp.text))
        raise


def construct_path(host, method):
    return urljoin(host, method)
