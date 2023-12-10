FROM --platform=linux/x86_64 python:3.11.2-slim-bullseye

USER 0
WORKDIR /app
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update \
    && apt-get install -y curl build-essential \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false
ENV PATH="/root/.cargo/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main

COPY app/ ./app/
COPY init-data.json ./init-data.json

EXPOSE 8000
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
