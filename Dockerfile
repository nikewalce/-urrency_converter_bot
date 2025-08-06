# 1. Используем официальный образ Python
FROM python:3.13

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# 4. Копируем зависимости и README в контейнер
COPY pyproject.toml poetry.lock* /app/

# 5. Копируем исходники
COPY src_bot /app/src_bot

# 6. Устанавливаем зависимости без виртуального окружения
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# 7. Копируем остальное
COPY . /app

# 8. Запуск
CMD ["python", "src_bot/main.py"]
