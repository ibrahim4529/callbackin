import pytest
from main import app


def test_app():
    assert app is not None

@pytest.mark.usefixtures("client")
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Callbackin API",
        "version": "0.1.0",
        "description": "A simple API to manage callbacks",
        "author": "Ibrahim Hanif (ibrahim4529)",
        "github": "https://github.com/ibrahim4529/callbackin"
    }