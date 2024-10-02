from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GetRoleByUUID(BaseModel):
    uuid: UUID


class CreateRole(BaseModel):
    name: str
    jdata: Optional[dict]


class RoleReturnData(GetRoleByUUID, CreateRole):
    created_at: datetime
    updated_at: datetime
