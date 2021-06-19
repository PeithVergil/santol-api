from .client import client
from .settings import USERS

from santol.authen import delete_user, delete_token


def test_users_create():
    """
    Running the test on its own:
    
        pytest tests/test_authen.py::test_users_create
    """
    user = USERS[0]

    response = client.post('/auth/users', json={
        'username': user['username'],
        'password': user['password'],
    })
    assert response.status_code == 200

    data = response.json()

    assert data['id']         is not None
    assert data['username']   is not None
    assert data['created_at'] is not None

    assert delete_user(data['id']) is True


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


def test_users_authenticate(users):
    """
    Running the test on its own:

        pytest tests/test_authen.py::test_users_authenticate
    """
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
