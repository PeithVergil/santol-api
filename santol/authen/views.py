from fastapi import HTTPException, Depends, security, status

from .app import app
from .models import UserToken, UserCredentials
from .functions import authenticate_credentials, generate_token


bearer = security.HTTPBearer()


@app.post('/authenticate')
def authenticate(credentials: UserCredentials) -> UserToken:
    user = authenticate_credentials(credentials)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    return generate_token(user)
