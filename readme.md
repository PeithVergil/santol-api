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

## Docker for Development

```bash
export SANTOL_API_ROOT=~/dev/santol-api
export SANTOL_API_VENV=~/venv/santol-api

# Install Python packages.
docker run -it --rm --name santol_api --workdir /app -v $SANTOL_API_ROOT:/app -v $SANTOL_API_VENV:/venv python:3.9-buster python -m venv /venv
docker run -it --rm --name santol_api --workdir /app -v $SANTOL_API_ROOT:/app -v $SANTOL_API_VENV:/venv python:3.9-buster /venv/bin/pip install -r requirements-dev.txt

# Start the dev server.
docker run --rm --detach --name santol_api --workdir /app -v $SANTOL_API_ROOT:/app -v $SANTOL_API_VENV:/venv --network dagnet --publish 8000:8000 python:3.9-buster /venv/bin/uvicorn santol:app --host 0.0.0.0 --reload

# Running the tests.
docker run -it --rm --name santol_test --workdir /app -v $SANTOL_API_ROOT:/app -v $SANTOL_API_VENV:/venv -e "SANTOL_DATABASE=testing" --network dagnet python:3.9-buster /venv/bin/pytest
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
