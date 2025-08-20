FROM python:3.13-slim

ENV PYTHONPATH=/app
WORKDIR /app

RUN pip install poetry

COPY pyproject.toml ./


RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "MyService.main:app", "--host", "0.0.0.0", "--port", "8000"]