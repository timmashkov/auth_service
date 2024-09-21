from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator, Field, EmailStr


class GetUserByUUID(BaseModel):
    uuid: UUID


class LoginUser(BaseModel):
    login: str
    password: str


class UpdateUser(BaseModel):
    login: str
    email: EmailStr
    age: int
    phone_number: str = Field(examples=["89986661488", "+79986661488"])

    @field_validator("age")
    def check_age(cls, value):
        if 1 <= value <= 100:
            return value
        raise ValueError("Age must be higher then 0 and less then 101")

    @field_validator("phone_number")
    def check_number(cls, value):
        if (value.isdigit() and len(value) == 11) or (
            value[1:].isdigit() and value.startswith("+") and len(value) == 12
        ):
            return value
        raise ValueError("Invalid phone number")


class CreateUser(UpdateUser, LoginUser):
    pass


class UserReturnData(GetUserByUUID, UpdateUser):
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserReturnFullData(UserReturnData):
    password: str
