import requests

API_BASE_URL = 'http://127.0.0.1:8000/'


def make_get_request(url, params):
    res = requests.get(url, params)

    return res


def make_post_request(url, payload, waiting=True):
    res = requests.post(url, payload)

    if waiting:
        return res


def make_put_request(url, payload, waiting):
    res = requests.put(url, payload)

    if waiting:
        return res