import pytest

from .client import client
from .settings import PROFILES

from santol.profile import delete_profile


@pytest.fixture
def create_profile_response(tokens, db):
    token = tokens[0]
    profile = PROFILES[0]

    response = client.post('/profiles/',
        json={
            'fname': profile['fname'],
            'lname': profile['lname'],
        },
        headers={
            'Authorization': f'Bearer {token.value}',
        },
    )

    yield response

    data = response.json()

    assert delete_profile(data['id'], db) is True


def test_profiles_create(create_profile_response):
    """
    Running the test on its own:
    
        pytest tests/test_profile.py::test_profiles_create
    """
    assert create_profile_response.status_code == 200

    data = create_profile_response.json()

    assert data['id']    is not None
    assert data['fname'] is not None
    assert data['lname'] is not None


def test_profiles_create_duplicate(tokens, profiles):
    """
    Running the test on its own:

        pytest tests/test_profile.py::test_profiles_create_duplicate
    """
    token = tokens[0]

    response = client.post('/profiles/',
        json={
            'fname': 'Jane',
            'lname': 'Doe',
        },
        headers={
            'Authorization': f'Bearer {token.value}',
        },
    )
    assert response.status_code == 400

    data = response.json()

    assert data['detail'] == 'Duplicate entry'


def test_profiles_detail(tokens, profiles):
    """
    Running the test on its own:
    
        pytest tests/test_profile.py::test_profiles_detail
    """
    token = tokens[0]
    profile = profiles[0]

    response = client.get('/profiles/me', headers={
        'Authorization': f'Bearer {token.value}',
    })
    assert response.status_code == 200

    data = response.json()

    assert data['id']    is not None
    assert data['fname'] == profile.fname
    assert data['lname'] == profile.lname


def test_profiles_detail_empty(tokens):
    """
    Running the test on its own:
    
        pytest tests/test_profile.py::test_profiles_detail_empty
    """
    token = tokens[0]

    response = client.get('/profiles/me', headers={
        'Authorization': f'Bearer {token.value}',
    })
    assert response.status_code == 404

    data = response.json()

    assert data['detail'] == 'Profile does not exist'
