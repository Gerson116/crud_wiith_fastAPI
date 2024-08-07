from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

#gt greater than
#ge greater than or equal
#lt less than
#le less than or equal

class userModel(BaseModel):
    user_id: int | None
    names: str = Field(min_length=3, max_length=50)
    lastname: str = Field(min_length=3, max_length=250)
    email: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=250)


class userModelCreate(BaseModel):
    names: str = Field(min_length=3, max_length=50)
    lastname: str = Field(min_length=3, max_length=250)
    email: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=250)

class userModelEdit(BaseModel):
    user_id: int | None
    names: str = Field(min_length=3, max_length=50)
    lastname: str = Field(min_length=3, max_length=250)
    email: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=250)
    statusId: int = Field(ge = 0)