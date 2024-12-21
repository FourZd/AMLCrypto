FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        libpq-dev \
        libssl-dev \
        libblas-dev \
        liblapack-dev \
        libc-dev \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы Poetry и устанавливаем зависимости
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry config installer.max-workers 10 \
    && poetry install --no-interaction --no-ansi \
    && poetry show

# Копируем весь проект
COPY . /app/

RUN poetry run python -m pytest tests/

# Команда для запуска приложения
CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]
