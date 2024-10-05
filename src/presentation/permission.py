from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from domain.permission.schema import (
    CreatePermission,
    GetPermissionByUUID,
    PermissionReturnData,
)
from service.permission import PermissionService


class PermissionRouter:
    api_router = APIRouter(prefix="/permission", tags=["Permission"])
    output_model: BaseModel = PermissionReturnData
    input_model: BaseModel = CreatePermission
    service_client: PermissionService = Depends(PermissionService)

    @staticmethod
    @api_router.get("/one", response_model=output_model)
    async def get(
        perm_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.get(cmd=GetPermissionByUUID(uuid=perm_uuid))

    @staticmethod
    @api_router.get("/all", response_model=List[output_model])
    async def get_list(
        parameter: str = "created_at",
        service=service_client,
    ) -> List[output_model]:
        return await service.get_list(parameter=parameter)

    @staticmethod
    @api_router.post("/create", response_model=output_model)
    async def create(
        incoming_data: CreatePermission,
        service=service_client,
    ) -> output_model:
        return await service.create(data=incoming_data)

    @staticmethod
    @api_router.patch("/update{role_uuid}", response_model=output_model)
    async def update(
        perm_uuid: str | UUID,
        incoming_data: CreatePermission,
        service=service_client,
    ) -> output_model:
        return await service.update(
            data=incoming_data, perm_uuid=GetPermissionByUUID(uuid=perm_uuid)
        )

    @staticmethod
    @api_router.delete("/delete", response_model=output_model)
    async def delete(
        perm_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.delete(perm_uuid=GetPermissionByUUID(uuid=perm_uuid))
