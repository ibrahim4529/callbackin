import pytest
from fastapi.testclient import TestClient
from models import User, Callback
from utils.jwt import create_access_token
from sqlmodel import Session


@pytest.mark.usefixtures("client", "session", "user")
def test_create_callback_sucess(client: TestClient,
                                user: User):
    """Test create callback
    1. Create dummy user
    2. Create dummy callback
    3. Assert callback is not None
    4. Assert callback id is 1
    5. Assert callback name is "Test"
    6. Assert callback user_id is same as user id
    """
    data_callback = {
        "name": "Test",
        "description": "Test",
        "local_endpoint": "http://localhost:8000/callbacks/1"
    }
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.post("/callbacks", json=data_callback)
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['id'] == 1
    assert response.json()['name'] == "Test"
    assert response.json()['user_id'] == user.id
    assert response.json()['description'] == "Test"


@pytest.mark.usefixtures("session", "user")
def test_create_callback_fail_request_not_valid(client: TestClient,
                                                user: User):
    """Test create callback
    1. Create dummy user
    2. Create dummy callback with invalid request
    3. Assert if throws 422
    4. Assert if throws field required
    """
    data_callback = {
        "description": "Test",
    }
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.post("/callbacks", json=data_callback)
    assert response.status_code == 422
    assert response.json() is not None
    assert response.json()['detail'][0]['msg'] == "field required"


@pytest.mark.usefixtures("client")
def test_create_callback_fail_user_not_authenticated(client):
    """Test create callback
    1. Create dummy callback
    2. Assert if throws 403
    3. Assert if throws Not authenticated
    """
    data_callback = {
        "name": "Test",
        "description": "Test",
    }
    response = client.post("/callbacks", json=data_callback)
    assert response.status_code == 403
    assert response.json() is not None
    assert response.json()['detail'] == "Not authenticated"


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_get_callbacks_sucess(client, session: Session, user: User, callback: Callback):
    """Test get callbacks
    1. Create dummy user use fixtures
    2. Create dummy callback use fixtures
    3. Assert if response is not None
    4. Assert if response is list
    5. Assert if response length is 1
    6. Assert if response id is 1
    7. Assert if response name is "Test"
    8. Assert if response user_id is same as user id
    """
    session.commit()
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.get("/callbacks")
    assert response.status_code == 200
    assert response.json() is not None
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == callback.id
    assert response.json()[0]['name'] == callback.name
    assert response.json()[0]['user_id'] == user.id
    assert response.json()[0]['description'] == callback.description


@pytest.mark.usefixtures("client", "session")
def test_get_callbacks_fail_user_not_authenticated(client, session: Session):
    """Test get callbacks
    1. Call get callbacks endpoint without authentication
    2. Assert if throws 403
    3. Assert if throws Not authenticated
    """
    session.commit()
    response = client.get("/callbacks")
    assert response.status_code == 403
    assert response.json() is not None
    assert response.json()['detail'] == "Not authenticated"


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_get_callback_sucess(client, session: Session, user: User, callback: Callback):
    """Test get callback by id
    1. Create dummy callback use fixtures
    2. Call get callback by id endpoint
    3. Assert if response is not None
    4. Assert if response data is same as dummy callback
    """
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.get(f"/callbacks/{callback.id}")
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['id'] == callback.id
    assert response.json()['name'] == "Test"
    assert response.json()['user_id'] == user.id
    assert response.json()['description'] == "Test"
    assert response.json()['is_running'] == callback.is_running
    assert response.json()['path'] == str(callback.path)


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_get_callback_fail_user_not_authenticated(client: TestClient,
                                                  session: Session,
                                                  user: User,
                                                  callback: Callback):
    """Test get callback by id
    1. Create dummy callback
    2. Call get callback by id endpoint
    3. Assert if throws 403
    4. Assert if throws Not authenticated
    """
    session.add(callback)
    session.commit()
    session.refresh(callback)
    response = client.get(f"/callbacks/{callback.id}")
    assert response.status_code == 403
    assert response.json() is not None
    assert response.json()['detail'] == "Not authenticated"


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_get_callback_fail_callback_not_found(client: TestClient,
                                              session: Session,
                                              user: User,
                                              callback: Callback):
    """Test get callback by id
    1. Create dummy callback
    2. Call get callback by id endpoint with invalid id
    3. Assert if throws 404
    4. Assert if throws Callback not found
    """
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.get(f"/callbacks/2")
    assert response.status_code == 404
    assert response.json() is not None
    assert response.json()['detail'] == "Callback not found"


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_edit_callback_success(client, session, user, callback):
    """Test edit callback
    1. Create dummy callback use fixtures
    2. Call edit callback endpoint
    3. Assert if response is not None
    4. Assert if response data is same as dummy callback
    """
    data_callback = {
        "name": "Test 2",
        "description": "Test 2",
        "local_endpoint": "http://localhost:8000/edited/path",
    }
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.put(f"/callbacks/{callback.id}", json=data_callback)
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['id'] == callback.id
    assert response.json()['name'] == "Test 2"
    assert response.json()['user_id'] == user.id
    assert response.json()['description'] == "Test 2"
    assert response.json()['is_running'] == callback.is_running


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_edit_callback_fail_user_not_authenticated(client, session, user, callback):
    """Test edit callback
    1. Create dummy callback use fixtures
    2. Call edit callback endpoint
    3. Assert if throws 403
    4. Assert if throws Not authenticated
    """
    data_callback = {
        "name": "Test 2",
        "description": "Test 2",
        "local_endpoint": "http://localhost:8000/edited/path",
    }
    response = client.put(f"/callbacks/{callback.id}", json=data_callback)
    assert response.status_code == 403
    assert response.json() is not None
    assert response.json()['detail'] == "Not authenticated"


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_edit_callback_fail_callback_not_found(client, session, user, callback):
    """Test edit callback
    1. Create dummy callback use fixtures
    2. Call edit callback endpoint with invalid id
    3. Assert if throws 404
    4. Assert if throws Callback not found
    """
    data_callback = {
        "name": "Test 2",
        "description": "Test 2",
        "local_endpoint": "http://localhost:8000/edited/path",
    }
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.put(f"/callbacks/2", json=data_callback)
    assert response.status_code == 404
    assert response.json() is not None
    assert response.json()['detail'] == "Callback not found"


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_delete_callback_success(client, session, user, callback):
    """Test delete callback
    1. Create dummy callback use fixtures
    2. Call delete callback endpoint
    3. Assert if response is not None
    4. Assert if response data is same as dummy callback
    """
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.delete(f"/callbacks/{callback.id}")
    assert response.status_code == 204


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_delete_callback_fail_user_not_authenticated(client, session, user, callback):
    """Test delete callback
    1. Create dummy callback use fixtures
    2. Call delete callback endpoint
    3. Assert if throws 403
    4. Assert if throws Not authenticated
    """
    response = client.delete(f"/callbacks/{callback.id}")
    assert response.status_code == 403
    assert response.json() is not None
    assert response.json()['detail'] == "Not authenticated"


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_delete_callback_fail_callback_not_found(client, session, user, callback):
    """Test delete callback
    1. Create dummy callback use fixtures
    2. Call delete callback endpoint with invalid id
    3. Assert if throws 404
    4. Assert if throws Callback not found
    """
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.delete(f"/callbacks/2")
    assert response.status_code == 404
    assert response.json() is not None
    assert response.json()['detail'] == "Callback not found"


@pytest.mark.usefixtures("client","user" ,"session", "callback")
def test_run_callback_success(client, user ,session, callback):
    """Test run callback
    1. Create dummy callback use fixtures
    2. Call run callback endpoint
    3. Assert if response is not None
    4. Assert if response data is same as dummy callback
    """
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.get(f"/callbacks/{callback.id}/run")
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['id'] == callback.id
    assert response.json()['name'] == callback.name
    assert response.json()['user_id'] == callback.user_id
    assert response.json()['description'] == callback.description
    assert response.json()['is_running'] == True


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_run_callback_fail_user_not_authenticated(client, session, user, callback):
    """Test run callback
    1. Create dummy callback use fixtures
    2. Call run callback endpoint
    3. Assert if throws 403
    4. Assert if throws Not authenticated
    """
    response = client.get(f"/callbacks/{callback.id}/run")
    assert response.status_code == 403
    assert response.json() is not None
    assert response.json()['detail'] == "Not authenticated"


@pytest.mark.usefixtures("client", "session", "user", "callback")
def test_run_callback_fail_callback_not_found(client, session, user, callback):
    """Test run callback
    1. Create dummy callback use fixtures
    2. Call run callback endpoint with invalid id
    3. Assert if throws 404
    4. Assert if throws Callback not found
    """
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.get(f"/callbacks/2/run")
    assert response.status_code == 404
    assert response.json() is not None
    assert response.json()['detail'] == "Callback not found"


@pytest.mark.usefixtures("client","user" ,"session", "callback")
def test_stop_callback_success(client, user ,session, callback):
    """Test stop callback
    1. Create dummy callback use fixtures
    2. Call stop callback endpoint
    3. Assert if response is not None
    4. Assert if response data is same as dummy callback
    """
    token = create_access_token(user.id)
    client.headers['Authorization'] = f"Bearer {token}"
    response = client.get(f"/callbacks/{callback.id}/stop")
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['id'] == callback.id
    assert response.json()['name'] == callback.name
    assert response.json()['user_id'] == callback.user_id
    assert response.json()['description'] == callback.description
    assert response.json()['is_running'] == False


@pytest.mark.usefixtures("client","callback")
def test_stop_callback_fail_user_not_authenticated(client, callback):
    """Test stop callback
    1. Create dummy callback use fixtures
    2. Call stop callback endpoint
    3. Assert if throws 403
    4. Assert if throws Not authenticated
    """
    response = client.get(f"/callbacks/{callback.id}/stop")
    assert response.status_code == 403
    assert response.json() is not None
    assert response.json()['detail'] == "Not authenticated"