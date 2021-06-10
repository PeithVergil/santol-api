from fastapi import Depends

from .app import app
from .models import ProfileInput, ProfileInfo
from .functions import select_profile, create_profile
from ..authen import UserInfo, authen_user


@app.get('/me')
def profiles_detail(user: UserInfo = Depends(authen_user)) -> ProfileInfo:
    return select_profile(user.id)


@app.post('/')
def profiles_create(profile: ProfileInput, user: UserInfo = Depends(authen_user)) -> ProfileInfo:
    return create_profile(user.id, profile.fname, profile.lname)


__all__ = [
    'profiles_detail',
    'profiles_create',
]
