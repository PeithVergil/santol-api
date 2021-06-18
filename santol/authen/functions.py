import base64
import hashlib
import logging
import secrets

from typing import Optional
from fastapi import HTTPException, Depends, security, status
from datetime import datetime, timedelta
from sqlalchemy import desc, exc

from .chems import User, Token
from .models import UserCredentials, UserInfo, UserToken
from ..errors import DatabaseError
from ..alchemy import AlchemySession
from ..settings import HASH_FUNC, HASH_ITER


logger = logging.getLogger(__name__)

bearer = security.HTTPBearer()


def password_hash(password, salt=None):
    salt = secrets.token_hex(8) if salt is None else salt
    hash = hashlib.pbkdf2_hmac(
        HASH_FUNC, password.encode(), salt.encode(),
        HASH_ITER
    )
    b16 = base64.b16encode(hash).decode()
    return '{}${}'.format(salt, b16)


def password_check(password, hashed_password):
    salt, hash = hashed_password.split('$')
    pass_hash = hashlib.pbkdf2_hmac(
        HASH_FUNC, password.encode(), salt.encode(),
        HASH_ITER
    )
    pass_b16 = base64.b16encode(pass_hash).decode()
    return pass_b16 == hash


def authenticate_credentials(credentials: UserCredentials) -> Optional[UserInfo]:
    with AlchemySession() as session:
        query = (
            session
            .query(User)
            .filter(User.username == credentials.username)
        )
        user = query.first()
        if user is not None:
            is_valid = password_check(credentials.password, user.password)
            if is_valid:
                return UserInfo.from_orm(user)
        return None


def create_user(username: str, password: str, session=None) -> UserInfo:
    password = password_hash(password)
    
    if session is not None:
        return ackchyually_create_user(username, password, session)
    
    with AlchemySession(False) as session:
        return ackchyually_create_user(username, password, session)


def ackchyually_create_user(username: str, password: str, session: AlchemySession) -> UserInfo:
    user = User(
        username=username,
        password=password,
        created_at=datetime.utcnow()
    )

    session.add(user)

    try:
        session.commit()
    except exc.IntegrityError as error:
        session.rollback()

        logger.exception('Failed to create a new user.')
        
        errnum, errmsg = error.orig.args
        title = 'Failed to create a new user.'
        info = {
            'code': errnum,
            'text': errmsg,
        }
        raise DatabaseError(info, title)

    return UserInfo.from_orm(user)


def delete_user(user_id: int, session=None) -> bool:
    if session is not None:
        return ackchyually_delete_user(user_id, session)
    
    with AlchemySession(False) as session:
        return ackchyually_delete_user(user_id, session)


def ackchyually_delete_user(user_id: int, session: AlchemySession) -> bool:
    query = (
        session
        .query(User)
        .filter(User.id == user_id)
    )

    query.delete()

    try:
        session.commit()
    except exc.IntegrityError as error:
        session.rollback()

        logger.exception('Failed to delete the user.')

        return False

    return True


def random_token(user: UserInfo) -> str:
    tkn, now = secrets.token_hex(16), datetime.utcnow()
    # Generate a random value which will
    # be used to create the session token.
    #
    # Example:
    # 123456$f4507f818b8d3aa2ef3ba5267e7abe7a$1623061671.622073
    value = '{}${}${}'.format(
        user.id, tkn, now.timestamp()
    )

    # The session token is a SHA256 hash of the above.
    return hashlib.sha256(value.encode()).hexdigest()


def create_token(user: UserInfo, session=None) -> UserToken:
    if session is not None:
        return ackchyually_create_token(user, session)
    
    with AlchemySession(False) as session:
        return ackchyually_create_token(user, session)


def ackchyually_create_token(user: UserInfo, session: AlchemySession) -> UserToken:
    created_at = datetime.utcnow()
    expired_at = datetime.utcnow() + timedelta(hours=1)

    token = Token(
        value=random_token(user),
        user_id=user.id,
        created_at=created_at,
        expired_at=expired_at,
    )

    session.add(token)

    try:
        session.commit()
    except exc.IntegrityError as error:
        session.rollback()

        logger.exception('Failed to create a user token.')

        errnum, errmsg = error.orig.args
        title = 'Failed to create a user token.'
        info = {
            'code': errnum,
            'text': errmsg,
        }
        raise DatabaseError(info, title)
    
    return UserToken.from_orm(token)


def delete_token(token: str, session=None) -> bool:
    if session is not None:
        return ackchyually_delete_token(token, session)
    
    with AlchemySession(False) as session:
        return ackchyually_delete_token(token, session)


def ackchyually_delete_token(token: str, session: AlchemySession) -> bool:
    query = (
        session
        .query(Token)
        .filter(Token.value == token)
    )

    query.delete()
    
    try:
        session.commit()
    except exc.IntegrityError as error:
        session.rollback()

        logger.exception('Failed to delete the user token.')

        return False

    return True


def authen_user(authorization: security.HTTPAuthorizationCredentials = Depends(bearer)) -> UserInfo:
    with AlchemySession(False) as session:
        query = (
            session
            .query(Token)
            .join(Token.user)
            .filter(Token.value == authorization.credentials)
            .order_by(desc(Token.created_at))
            .limit(1)
        )
        token = query.first()

        if token is None:
            logger.info('Token not found.')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Token does not exist')
        
        return UserInfo.from_orm(token.user)
