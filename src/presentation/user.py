from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from domain.user.schema import GetUserByUUID, UserReturnData, CreateUser, UpdateUser
from service.user import UserService


class UserRouter:
    api_router = APIRouter(prefix="/user", tags=["User"])
    output_model: BaseModel = UserReturnData
    input_model: BaseModel = CreateUser
    service_client: UserService = Depends(UserService)

    @staticmethod
    @api_router.get("/one", response_model=output_model)
    async def show_user(
        user_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.get(cmd=GetUserByUUID(uuid=user_uuid))

    @staticmethod
    @api_router.get("/all", response_model=List[output_model])
    async def get_users(
        parameter: str = "created_at",
        service=service_client,
    ) -> List[output_model]:
        return await service.get_list(parameter=parameter)

    @staticmethod
    @api_router.post("/create", response_model=output_model)
    async def create(
        incoming_data: CreateUser,
        service=service_client,
    ) -> output_model:
        return await service.create(data=incoming_data)

    @staticmethod
    @api_router.patch("/update{user_uuid}", response_model=output_model)
    async def update(
        user_uuid: str | UUID,
        incoming_data: UpdateUser,
        service=service_client,
    ) -> output_model:
        return await service.update(
            data=incoming_data, user_uuid=GetUserByUUID(uuid=user_uuid)
        )

    @staticmethod
    @api_router.delete("/delete", response_model=output_model)
    async def delete(
        user_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.delete(user_uuid=GetUserByUUID(uuid=user_uuid))
