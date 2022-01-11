from _pytest.fixtures import fixture
from fastapi.testclient import TestClient
from app.database import get_db, Base
import pytest
from app import models
from app.oauth import create_access_token
from app.main import app
from app.config import setting
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionlocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='function')
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='function')
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope='function')
def test_user1(client):
    user_data = {"email": "crab123@gmail.com", "password": '321123'}
    res = client.post(
        '/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture(scope='function')
def test_user(client):
    user_data = {"email": "crab@gmail.com", "password": '321123'}
    res = client.post(
        '/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    res = create_access_token({"email":test_user['email']})
    return res


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def token1(test_user1):
    res = create_access_token({"email": test_user1['email']})
    return res


@pytest.fixture
def authorized_client1(client, token1):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token1}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st con",
            "owner_email": test_user['email']
        },
        {
            "title": "2nd title",
            "content": "2nd con",
            "owner_email": test_user['email']
        },
        {
            "title": "3rd title",
            "content": "3rd con",
            "owner_email": test_user['email']
        }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    post = session.query(models.Post).all()
    return post
