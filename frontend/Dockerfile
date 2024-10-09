FROM node:22.8.0-alpine3.20 AS build

WORKDIR /app

ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

COPY package*.json ./

RUN npm install --frozen-lockfile

COPY . .

RUN npm run build


FROM python:3.12-alpine3.20

WORKDIR /app

COPY ./server .

COPY --from=build /app/dist ./static

RUN pip install poetry

RUN poetry install --no-root

CMD ["poetry", "run", "uvicorn", "--host=0.0.0.0", "--port=8080", "app:app"]
