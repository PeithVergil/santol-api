from .app import app
from .authen import app as authen
from .profile import app as profile


app.mount('/auth', authen)
app.mount('/profiles', profile)


__all__ = [
    'app',
]
