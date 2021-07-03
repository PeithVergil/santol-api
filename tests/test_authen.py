import pytest

from .client import client
from .settings import USERS

from santol.authen import delete_user, delete_token


@pytest.fixture
def create_user_response(db):
    user = USERS[0]

    response = client.post('/auth/users', json={
        'username': user['username'],
        'password': user['password'],
    })

    yield response

    data = response.json()

    assert delete_user(data['id'], db) is True


def test_users_create(create_user_response):
    """
    Running the test on its own:
    
        pytest tests/test_authen.py::test_users_create
    """
    assert create_user_response.status_code == 200

    data = create_user_response.json()

    assert data['id']         is not None
    assert data['username']   is not None
    assert data['created_at'] is not None


def test_users_create_duplicate(users):
    """
    Running the test on its own:

        pytest tests/test_authen.py::test_users_create_duplicate
    """
    user = USERS[0]

    response = client.post('/auth/users', json={
        'username': user['username'],
        'password': user['password'],
    })
    assert response.status_code == 400

    data = response.json()

    assert data['detail'] == 'Duplicate entry'


@pytest.fixture
def authenticate_user(users, db):
    user = USERS[0]

    response = client.post('/auth/authenticate', json={
        'username': user['username'],
        'password': user['password'],
    })

    yield response

    data = response.json()

    assert delete_token(data['value'], db) is True


def test_users_authenticate(authenticate_user):
    """
    Running the test on its own:

        pytest tests/test_authen.py::test_users_authenticate
    """
    assert authenticate_user.status_code == 200

    data = authenticate_user.json()

    assert data['value']      is not None
    assert data['created_at'] is not None
    assert data['expired_at'] is not None
