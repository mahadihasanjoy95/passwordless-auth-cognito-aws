import json
from datetime import datetime
from http import HTTPStatus
from typing import Optional, Any, Dict, List

import pydantic
from pydantic import BaseModel, Field, validator

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

app = APIGatewayRestResolver()
logger = Logger(service="APP")


class UserModel(BaseModel):
    username: str = Field(..., max_length=10)
    password1: str
    password2: str

    @validator('password1', each_item=True)
    def check_names_not_empty(cls, v):
        assert v != '', 'Empty strings are not allowed.'
        return v


class EventBridgeModel(BaseModel):
    version: str
    id: str
    detail_type: str = Field(None)
    source: str
    account: str
    time: datetime
    region: str
    resources: List[str]
    detail: UserModel


@app.get("/powertools/<name>")
def hello_name(name):
    logger.info(f"Request from {name} received")
    return {"message": f"hello {name}!"}


@app.post("/post/powertool")
def hello_post():
    # data: dict = app.current_event.json_body

    try:
        parsed_event = EventBridgeModel(**app.current_event.json_body)
        print(f'got username {parsed_event.detail.username}')
        print(f'got password {parsed_event.detail.password1}')
        return {
            "statusCode": HTTPStatus.OK,
            "body": json.loads(parsed_event.detail.json()),
        }
    except pydantic.ValidationError as ex:
        logger.error(f'validation error, error={ex}')
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": json.loads(ex.json())
        }


@app.get("/powertools")
def hello():
    logger.info("Request from unknown received")
    return {"message": "hello unknown!"}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
def lambda_handler(event: Dict[str, Optional[Any]], context):
    return app.resolve(event, context)
