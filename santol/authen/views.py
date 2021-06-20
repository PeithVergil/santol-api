from fastapi import HTTPException, security, status

from .app import router
from .models import UserInfo, UserToken, UserCredentials
from .functions import authenticate_credentials, create_token, create_user
from ..errors import DatabaseError


@router.post('/auth/users')
def users_create(credentials: UserCredentials) -> UserInfo:
    try:
        user = create_user(credentials.username, credentials.password)
    except DatabaseError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.detail)
    return user


@router.post('/auth/authenticate')
def users_authenticate(credentials: UserCredentials) -> UserToken:
    user = authenticate_credentials(credentials)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    return create_token(user)


__all__ = [
    'users_create',
    'users_authenticate',
]
