import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from utils.db import get_session
from main import app
from models import User, Callback


client = TestClient(app)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="user")
def dummy_user_fixture(session: Session):
    user = User(
        email="testuser@mail.com",
        password="password",
        full_name="Test User",
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="callback")
def dummy_callback_fixture(session: Session, user: User):
    callback = Callback(
        name="Test",
        description="Test",
        user_id=user.id,
        local_endpoint="http://localhost:8000/callbacks/1"
    )
    session.add(callback)
    session.commit()
    session.refresh(callback)
    print(callback)
    return callback
