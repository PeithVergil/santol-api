Santol API
==========

A demo RESTful API built using Python's FastAPI framework.


Starting the server for development.

```bash
uvicorn santol:app --reload
```

Running tests.

```bash
pytest
```

## Deployment

```bash
pip install -r requirements-prod.txt
```

```bash
gunicorn santol:app -w 4 -b 127.0.0.1:8000 -k uvicorn.workers.UvicornWorker
```