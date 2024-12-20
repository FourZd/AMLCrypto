FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry config installer.max-workers 3 \
    && poetry install --no-interaction --no-ansi

COPY . /app/

CMD ["bash", "-c", "poetry run python3 main.py"]
