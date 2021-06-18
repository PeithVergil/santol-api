from fastapi.testclient import TestClient

from santol import app

client = TestClient(app)
