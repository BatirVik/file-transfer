from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.logger import logger, logger_middleware
from app.config import config
from app.aws import logs, s3
from app.api import v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    await s3.create_bucket(config.S3_BUCKET_NAME)
    await logs.create_log_group(config.LOGS_LOG_GROUP_NAME)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(v1.router)

logger.remove(0)
app.middleware("http")(logger_middleware)

origins = [
    "http://0.0.0.0:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")
