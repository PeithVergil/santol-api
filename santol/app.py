from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import Profile


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        'http://localhost:8080',
        'http://127.0.0.1:8080',
        'http://192.168.254.102:8080',
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home_root():
    return {'page': 'Home'}

@app.get('/profiles')
def profile_list(limit: int = 10):
    return [
        Profile(name='Jane Doe', email='jane.doe@example.com'),
        Profile(name='Jean Doe', email='jean.doe@example.com'),
        Profile(name='Jena Doe', email='jena.doe@example.com'),
    ]

@app.post('/profiles')
def profile_create(profile: Profile):
    return profile

@app.post('/profiles/{pk}')
def profile_detail(pk: int):
    return Profile(name='Jane Doe', email=f'jane.doe.{pk}@example.com'),
