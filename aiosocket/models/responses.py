from pydantic import BaseModel
from typing import Dict, Any


class RequestModel(BaseModel):
    client: str
    hmac: str
    data: Dict[str, Any] = {}
    timestamp: str
    type: str


class ResponseModel(BaseModel):
    status: bool = True
    message: str
    data: Dict[str, Any] = {}
    type: str = "response"
