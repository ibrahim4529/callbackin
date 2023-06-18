import requests
from callbackin.utils.config import get_config



def get_base_url() -> str:
    config = get_config()
    if config["DEFAULT"]["base_url"] == "":
        raise Exception(
            "Base URL is not set, please run callbackin init")
    return config["DEFAULT"]["base_url"]


def get_token() -> str:
    config = get_config()
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
    return requests.get(get_base_url() + path, headers=headers, params=params)


def post(path: str, data={}):
    """ Simple wrapper for requests.post
    path: str - path to the endpoint
    data: dict
    """
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.post(get_base_url() + path, headers=headers, json=data)


def delete(path: str):
    """ Simple wrapper for requests.delete
    path: str - path to the endpoint
    """
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.delete(get_base_url() + path, headers=headers)


def put(path: str, data={}):
    """ Simple wrapper for requests.put
    path: str - path to the endpoint
    data: dict
    """
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.put(get_base_url() + path, headers=headers, json=data)
