# Backend

## Enviroment variables
**ENV**
> Based on this value, the configuration will load a specific .env file from the configuration folder. \
Available values: **production** (.env), **development** (.env.dev), **test** (.env.test)

**DB_URL**
> The URL of the database

**AWS_ACCESS_KEY**
> The AWS access key ID used alongside the secret key for API authentication.

**AWS_SECRET_KEY**
> The AWS secret access key for authenticating API requests.

**AWS_REGION_NAME**
> The AWS region where services are hosted.

**AWS_ENDPOINT_URL** / optional
> The custom endpoint URL for AWS services

**S3_BUCKET_NAME**
>  The name of the S3 bucket used for storing uploaded files.

**LOGS_LOG_GROUP_NAMA**
>  The name of the log group for storing logs in AWS CloudWatch.

## Run server
Activate the virtual environment
```bash
poetry shell
```
Install dependencies
```bash
poetry install --no-root
```
Define the ENV variable
```bash
export ENV=development
```
Populate the configuration/**.env.dev**
```env
DB_URL=...
AWS_ACCESS_KEY=...
AWS_SECRET_KEY=...
S3_BUCKET_NAME=...
AWS_REGION_NAME=...
LOGS_LOG_GROUP_NAME=...
```
Start uvicorn server
```bash
uvicorn app.main:app
```

## Testing
Run a postgresql docker
```bash
docker run -d -p 5100:5432 -e POSTGRES_DB=test -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test postgres
```
Run a localstack docker
```bash
poetry run localstack -d -e SERVICES=s3,logs -e AWS_ACCESS_KEY=test -e AWS_SECRET_KEY=test -e AWS_REGION_NAME=us-east-1 -e S3_BUCKET_NAME=test -e LOGS_LOG_GROUP_NAME=test
```
Populate the configuration/**.env.test** file
```env
DB_URL="postgresql+psycopg://test:test@localhost:5100/test"
AWS_ACCESS_KEY="test"
AWS_SECRET_KEY="test"
AWS_ENDPOINT_URL="http://localhost.localstack.cloud:4566"
S3_BUCKET_NAME="test"
AWS_REGION_NAME="us-east-1"
LOGS_LOG_GROUP_NAME="test"
```
Run pytest (ENV will be overridden to 'test' even if it was exported with a different value)
```bash
poetry run pytest
```

## Migrations
Define the ENV variable if you not,
```bash
export ENV=development
```
Create a migration file
```bash
poetry run alembic revision --autogenerate -m "message"
```
Apply migrations to the database based on the ENV variable
```bash
poetry run alembic upgrade head
```
