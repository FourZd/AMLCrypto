FROM python:3.12-slim

WORKDIR /app

# Установим зависимости для Python, включая Poetry
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы для Poetry
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry и проверяем успешность
RUN pip install poetry \
    && poetry --version || { echo "Poetry не установлен!"; exit 1; }

# Настраиваем Poetry и устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry config installer.max-workers 3 \
    && echo "Устанавливаем зависимости через poetry install" \
    && poetry install --no-interaction --no-ansi || { echo "Ошибка установки зависимостей"; exit 1; }

# Логируем установленные пакеты для проверки
RUN poetry show || { echo "Ошибка: Poetry не показывает пакеты"; exit 1; }

# Копируем исходный код в контейнер
COPY . /app/

# Проверяем, что файл main.py существует
RUN test -f main.py || { echo "Ошибка: main.py не найден"; exit 1; }

# Запуск с логированием
CMD ["bash", "-c", "echo 'Запуск приложения...'; poetry run python3 main.py || { echo 'Ошибка при запуске main.py'; exit 1; }"]
