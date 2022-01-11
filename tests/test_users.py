import pytest
from app.schemas import Token, UserResponse
from jose import jwt
from app.config import setting


def test_user_create(client):
    res = client.post(
        '/users/', json={"email": "user@example.com", "password": "234432"})
    asds = UserResponse(**res.json())
    assert asds.email == "user@example.com"
    res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        '/login', data={"username": test_user['email'], "password": test_user['password']})
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         setting.secret_key, algorithms=[setting.algorithm])
    email = payload.get('email')

    assert email == test_user['email']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email ,password ,status_code", [
    ('crab@gmail.com', '321123', 200),
    ('crab@gmail.com', 'wrong', 403),
    ('wrong@gmail.com', '321123', 403),
    ('wrong@gmail.com', 'wrong', 403),
    (None, '321123', 422),
    ('crab@gmail.com', None, 422)
])
def test_login_incorrect(test_user, client, email, password, status_code):
    res = client.post(
        '/login', data={"username": email, "password": password})
    assert res.status_code == status_code
