from fastapi import Depends

from .app import app
from .chems import Profile
from .models import ProfileInfo
from .functions import select_profile


@app.get('/me')
def me(profile: ProfileInfo = Depends(select_profile)) -> ProfileInfo:
    return profile
