

from fastapi import FastAPI
from pydantic import BaseModel

class OperationResult(BaseModel):
    Success: bool
    Message: str
    MessageDetail: str
    Data: set