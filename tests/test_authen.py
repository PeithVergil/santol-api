import pytest

from .client import client
from .settings import USERS

from santol.authen import create_user, delete_user, delete_token
from santol.alchemy import AlchemySession


@pytest.fixture()
def users():
    with AlchemySession(False) as session:
        _users = [
            create_user(
                _user['username'],
                _user['password'],
                session
            )
            for _user in USERS
        ]

        yield _users

        for _user in _users:
            delete_user(_user, session)


def test_authenticate(users):
    user = USERS[0]

    response = client.post('/auth/authenticate', json={
        'username': user['username'],
        'password': user['password'],
    })
    assert response.status_code == 200

    data = response.json()

    assert data['value']      is not None
    assert data['created_at'] is not None
    assert data['expired_at'] is not None

    assert delete_token(data['value']) is True
