from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class GetUserByUUID(BaseModel):
    uuid: UUID


class GetUserByNickname(BaseModel):
    nickname: str


class UserData(GetUserByNickname):
    first_name: str
    last_name: str
    patronymic: str
    age: int
    is_verified: bool = False

    @field_validator("age")
    def check_age(cls, value):
        if 1 <= value <= 100:
            return value
        raise ValueError("Age must be higher then 0 and less then 101")


class UserReturnData(GetUserByUUID, UserData):
    created_at: datetime
    updated_at: datetime
