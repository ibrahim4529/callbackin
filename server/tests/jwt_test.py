from jose import jwt
from utils.jwt import create_access_token
from utils.config import get_config

config = get_config()


def test_create_token_valid():
    """Test create_access_token
    1. Create access token
    2. Decode access token
    3. Assert access token is not None
    4. Assert payload id is 1
    """
    token = create_access_token(1)
    payload = jwt.decode(token, key=config.SECRET_KEY, algorithms="HS256")
    assert token is not None
    assert payload['id'] == 1


def test_create_token_invalid():
    """Test create_access_token
    1. Create access token
    2. Decode access token
    3. Assert access token is not None
    4. Assert payload id is 1
    """
    token = create_access_token(1)
    payload = jwt.decode(token, key=config.SECRET_KEY, algorithms="HS256")
    assert token is not None
    assert payload['id'] != 2


def test_create_token_invalid_key():
    """Test create_access_token
    1. Create access token
    2. Decode access token
    3. Assert if throws JWTError
    """
    token = create_access_token(1)
    try:
        payload = jwt.decode(token, key="invalid", algorithms="HS256")
    except Exception as e:
        assert e is not None
        assert e.__class__.__name__ == "JWTError"
    