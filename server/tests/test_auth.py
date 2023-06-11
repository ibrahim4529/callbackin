import pytest
from fastapi.testclient import TestClient
from models import User
from utils.jwt import create_access_token

@pytest.mark.usefixtures("client", "user")
def test_auth_success(client: TestClient, user: User):
    """ Test auth success
    1. Create token from dummy user
    2. Call auth/me endpoint with token
    3. Assert response status code is 200
    4. Assert response json is not None
    5. Assert response json email is same as dummy user email
    """
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.get("/auth/me")
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['email'] == user.email


@pytest.mark.usefixtures("client")
def test_auth_fail_user_not_authenticated(client: TestClient):
    """ Test auth fail user not authenticated
    1. Call auth/me endpoint without token
    2. Assert response status code is 403
    3. Assert response json is not None
    4. Assert response json detail is Not authenticated
    """
    response = client.get("/auth/me")
    assert response.status_code == 403
    assert response.json() is not None
    assert response.json()['detail'] == "Not authenticated"