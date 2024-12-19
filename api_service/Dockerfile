FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libpq-dev \
        gettext \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry config installer.max-workers 10 \
    && poetry install --no-interaction --no-ansi \
    && poetry show

COPY . /app/

RUN chmod +x /app/startup_scripts/entrypoint.sh
RUN chmod +x /app/startup_scripts/wait-for-it.sh

ENTRYPOINT ["/app/startup_scripts/entrypoint.sh"]
