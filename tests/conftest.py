import pytest

from .settings import USERS, PROFILES

from santol.authen import (
    create_user,
    delete_user,
    create_token,
    delete_token,
)
from santol.alchemy import SessionMaker, Session
from santol.profile import (
    create_profile,
    delete_profile,
)


@pytest.fixture()
def db():
    session = SessionMaker()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def users(db: Session):
    _users = [
        create_user(
            _user['username'],
            _user['password'],
            db
        )
        for _user in USERS
    ]

    yield _users

    for _user in _users:
        delete_user(_user.id, db)


@pytest.fixture()
def tokens(users, db: Session):
    _tokens = [
        create_token(user, db) for user in users
    ]

    yield _tokens

    for _token in _tokens:
        delete_token(_token.value, db)


@pytest.fixture()
def profiles(users, db: Session):
    _profiles = [
        create_profile(
            _user.id,
            _profile['fname'],
            _profile['lname'],
            db
        )
        for _user, _profile in zip(users, PROFILES)
    ]

    yield _profiles

    for _profile in _profiles:
        delete_profile(_profile.id, db)


__all__ = [
    'users',
    'tokens',
    'profiles',
]
