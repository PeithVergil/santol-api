import pytest

from .settings import USERS, PROFILES

from santol.authen import (
    create_user,
    delete_user,
    create_token,
    delete_token,
)
from santol.alchemy import AlchemySession
from santol.profile import (
    create_profile,
    delete_profile,
)


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
            delete_user(_user.id, session)


@pytest.fixture()
def tokens(users):
    with AlchemySession(False) as session:
        _tokens = [
            create_token(user, session) for user in users
        ]

        yield _tokens

        for _token in _tokens:
            delete_token(_token.value, session)


@pytest.fixture()
def profiles(users):
    with AlchemySession(False) as session:
        _profiles = [
            create_profile(
                _user.id,
                _profile['fname'],
                _profile['lname'],
                session
            )
            for _user, _profile in zip(users, PROFILES)
        ]

        yield _profiles

        for _profile in _profiles:
            delete_profile(_profile.id, session)


__all__ = [
    'users',
    'tokens',
    'profiles',
]
