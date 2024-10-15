FROM python:3.12-alpine3.20

WORKDIR /app

RUN apk add --no-cache postgresql-dev

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install --only main

COPY . .

ENV TZ=UTC

CMD ["poetry", "run", "uvicorn", "app.main:app", "--reload", "--host=0.0.0.0", "--port=8000", ]
