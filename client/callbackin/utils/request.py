import requests
from callbackin.utils.config import get_config

config = get_config()
BASE_URL = config["DEFAULT"]["base_url"]


def get_token() -> str:
    if config["DEFAULT"]["user_token"] == "":
        raise Exception(
            "You are not authenticated, please login first, using callbackin login")
    return config["DEFAULT"]["user_token"]


def get(path: str, params={}):
    """ Simple wrapper for requests.get
    path: str - path to the endpoint
    params: dict
    """
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.get(BASE_URL + path, headers=headers, params=params)


def post(path: str, data={}):
    """ Simple wrapper for requests.post
    path: str - path to the endpoint
    data: dict
    """
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.post(BASE_URL + path, headers=headers, json=data)


def delete(path: str):
    """ Simple wrapper for requests.delete
    path: str - path to the endpoint
    """
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.delete(BASE_URL + path, headers=headers)


def put(path: str, data={}):
    """ Simple wrapper for requests.put
    path: str - path to the endpoint
    data: dict
    """
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.put(BASE_URL + path, headers=headers, json=data)
