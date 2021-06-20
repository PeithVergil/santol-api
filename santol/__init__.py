from .app import app
from .authen import router as authen_router
from .profile import router as profile_router


app.include_router(authen_router)
app.include_router(profile_router)


__all__ = [
    'app',
]
