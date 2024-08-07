from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

#gt greater than
#ge greater than or equal
#lt less than
#le less than or equal

class LandscapeModel(BaseModel):
    landscape_id: int | None
    names: str = Field(min_length=3, max_length=50)
    direction: str = Field(min_length=3, max_length=250)
    description: str = Field(min_length=3, max_length=500)
    route: str | None
    statusId: int


class LandscapeModelCreate(BaseModel):
    names: str = Field(min_length=3, max_length=50)
    direction: str = Field(min_length=3, max_length=250)
    description: str = Field(min_length=3, max_length=500)
    route: str | None

class LandscapeModelEdit(BaseModel):
    names: str = Field(min_length=3, max_length=50)
    direction: str = Field(min_length=3, max_length=250)
    description: str = Field(min_length=3, max_length=500)
    route: str | None
    statusId: str = Field(min_length=1)