from fastapi import HTTPException, Depends, status

from .app import router
from .models import ProfileInput, ProfileInfo
from .functions import select_profile, create_profile
from ..authen import UserInfo, authen_user
from ..errors import DatabaseError
from ..alchemy import Session, alchemy_session


@router.get('/profiles/me')
def profiles_detail(user: UserInfo = Depends(authen_user), db: Session = Depends(alchemy_session)) -> ProfileInfo:
    return select_profile(user.id, db)


@router.post('/profiles/')
def profiles_create(profile: ProfileInput, user: UserInfo = Depends(authen_user), db: Session = Depends(alchemy_session)) -> ProfileInfo:
    try:
        return create_profile(user.id, profile.fname, profile.lname, db)
    except DatabaseError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.detail)


__all__ = [
    'profiles_detail',
    'profiles_create',
]
