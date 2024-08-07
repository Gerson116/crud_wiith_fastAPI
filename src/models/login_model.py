from email_validator import EmailNotValidError
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, field_validator

#gt greater than
#ge greater than or equal
#lt less than
#le less than or equal

# @field_validator("email")
# @classmethod
# def validate_email(cls, value):
#     try:
#         validate_email(value)
#     except EmailNotValidError:
#         raise ValueError("Invalid email format")
#     return value

class loginModel(BaseModel):
    email: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=250)