from fastapi import HTTPException, Depends, status

from .app import router
from .models import UserInfo, UserToken, UserCredentials
from .functions import authenticate_credentials, create_token, create_user
from ..errors import DatabaseError
from ..alchemy import Session, alchemy_session


@router.post('/auth/users')
def users_create(credentials: UserCredentials, db: Session = Depends(alchemy_session)) -> UserInfo:
    try:
        user = create_user(credentials.username, credentials.password, db)
    except DatabaseError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.detail)
    return user


@router.post('/auth/authenticate')
def users_authenticate(credentials: UserCredentials, db: Session = Depends(alchemy_session)) -> UserToken:
    user = authenticate_credentials(credentials, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    return create_token(user)


__all__ = [
    'users_create',
    'users_authenticate',
]
