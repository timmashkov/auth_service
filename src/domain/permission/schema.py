from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GetPermissionByUUID(BaseModel):
    uuid: UUID


class CreatePermission(BaseModel):
    name: str
    layer: str
    role_uuid: UUID
    jdata: Optional[dict]


class PermissionReturnData(GetPermissionByUUID, CreatePermission):
    created_at: datetime
    updated_at: datetime
