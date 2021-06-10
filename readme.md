Santol API
==========

A demo RESTful API built using Python's FastAPI framework.

## Development

Install required Python packages.

```bash
pip install -r requirements-dev.txt
```

Starting the server for development.

```bash
uvicorn santol:app --reload
```

Running tests.

```bash
SANTOL_DATABASE=testing pytest
```

## Deployment

Install required Python packages.

```bash
pip install -r requirements-prod.txt
```

Starting the server for production.

```bash
gunicorn santol:app -w 4 -b 127.0.0.1:8000 -k uvicorn.workers.UvicornWorker
```