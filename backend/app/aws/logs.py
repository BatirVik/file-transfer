from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING
import time
import functools

from botocore.exceptions import ClientError

if TYPE_CHECKING:
    from types_aiobotocore_logs.client import CloudWatchLogsClient

from app.config import config

from .session import session


@asynccontextmanager
async def get_logs_client() -> AsyncGenerator["CloudWatchLogsClient"]:
    async with session.client("logs", endpoint_url=config.AWS_ENDPOINT_URL) as client:
        yield client


async def create_log_stream(log_stream_name: str) -> None:
    async with get_logs_client() as client:
        try:
            await client.create_log_stream(
                logGroupName=config.LOGS_LOG_GROUP_NAME, logStreamName=log_stream_name
            )
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", None)
            if error_code != "ResourceAlreadyExistsException":
                raise e


async def create_log_group(log_group_name: str) -> None:
    async with get_logs_client() as client:
        try:
            await client.create_log_group(logGroupName=log_group_name)
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", None)
            if error_code != "ResourceAlreadyExistsException":
                raise e


async def logs_handler(message):
    async with get_logs_client() as client:
        log_group_name = config.LOGS_LOG_GROUP_NAME
        log_stream_name = time.strftime("%Y-%m-%d")

        descripe_log_stream = functools.partial(
            client.describe_log_streams,
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name,
            limit=1,
        )

        response = await descripe_log_stream()
        if not response["logStreams"]:
            await create_log_stream(log_stream_name)
            response = await descripe_log_stream()

        log_event = {
            "logGroupName": log_group_name,
            "logStreamName": log_stream_name,
            "logEvents": [
                {
                    "timestamp": int(message.record["time"].timestamp() * 1000),
                    "message": message,
                }
            ],
        }
        if token := response["logStreams"][0].get("uploadSequenceToken", None):
            log_event["sequenceToken"] = token

        await client.put_log_events(**log_event)
