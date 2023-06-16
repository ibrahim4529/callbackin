import pytest
from sqlmodel import Session
from models import CallbackHistory

@pytest.mark.usefixtures("client", "callback", "session")
def test_handle_callback(client, callback, session):
    """
    Test handle callback
    1. Call handle callback endpoint with callback path
    """
    header = '{"host": "testserver", "accept": "*/*", "accept-encoding": "gzip, deflate", "connection": "keep-alive", "user-agent": "testclient", "content-length": "16", "content-type": "application/json"}'
    response_post = client.post(f"/handle/{callback.path}", json={"test": "test"})
    assert response_post.status_code == 200
    _new_callback_history = session.query(CallbackHistory).filter(CallbackHistory.callback_id == callback.id).first()
    assert _new_callback_history is not None
    assert _new_callback_history.body == '{"test": "test"}'
    assert _new_callback_history.headers == header
    response_get = client.get(f"/handle/{callback.path}")
    assert response_get.status_code == 200
    response_put = client.put(f"/handle/{callback.path}", json={"test": "test"})
    assert response_put.status_code == 200

