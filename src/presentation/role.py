from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from domain.role.schema import CreateRole, GetRoleByUUID, RoleReturnData
from service.role import RoleService


class RoleRouter:
    api_router = APIRouter(prefix="/role", tags=["Role"])
    output_model: BaseModel = RoleReturnData
    input_model: BaseModel = CreateRole
    service_client: RoleService = Depends(RoleService)

    @staticmethod
    @api_router.get("/one", response_model=output_model)
    async def get(
        role_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.get(cmd=GetRoleByUUID(uuid=role_uuid))

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
        incoming_data: CreateRole,
        service=service_client,
    ) -> output_model:
        return await service.create(data=incoming_data)

    @staticmethod
    @api_router.patch("/update{role_uuid}", response_model=output_model)
    async def update(
        role_uuid: str | UUID,
        incoming_data: CreateRole,
        service=service_client,
    ) -> output_model:
        return await service.update(
            data=incoming_data, role_uuid=GetRoleByUUID(uuid=role_uuid)
        )

    @staticmethod
    @api_router.delete("/delete", response_model=output_model)
    async def delete(
        role_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.delete(role_uuid=GetRoleByUUID(uuid=role_uuid))
