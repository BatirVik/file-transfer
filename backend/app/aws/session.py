from aioboto3.session import Session
from app.config import config

session = Session(
    config.AWS_ACCESS_KEY,
    config.AWS_SECRET_KEY,
    region_name=config.AWS_REGION_NAME,
)
