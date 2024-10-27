from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from domain.user.schema import CreateUser, GetUserByUUID, LoginUser, UpdateUser, UserReturnData, UserTokenResult
from infrastructure.base_entities.base_model import BaseResultModel
from service.authenticate import AuthService


class AuthRouter:
    api_router = APIRouter(prefix="/auth", tags=["Auth"])
    output_model: BaseModel = UserReturnData
    input_model: BaseModel = CreateUser
    service_client: AuthService = Depends(AuthService)

    @staticmethod
    @api_router.post("/register", response_model=output_model)
    async def register(
        incoming_data: CreateUser,
        service=service_client,
    ) -> output_model:
        return await service.register(data=incoming_data)

    @staticmethod
    @api_router.patch("/edit{user_uuid}", response_model=output_model)
    async def edit(
        user_uuid: str | UUID,
        incoming_data: UpdateUser,
        service=service_client,
    ) -> output_model:
        return await service.edit_user(
            data=incoming_data, user_uuid=GetUserByUUID(uuid=user_uuid)
        )

    @staticmethod
    @api_router.delete("/delete/{user_uuid}", response_model=output_model)
    async def delete_user(
        user_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.delete_user(user_uuid=GetUserByUUID(uuid=user_uuid))

    @staticmethod
    @api_router.post("/login", response_model=UserTokenResult)
    async def login_user(
        cmd: LoginUser,
        service=service_client,
    ) -> UserTokenResult:
        return await service.login_user(cmd=cmd)

    @staticmethod
    @api_router.post("/logout", response_model=BaseResultModel)
    async def logout_user(
        refresh_token: str,
        service=service_client,
    ) -> BaseResultModel:
        return await service.logout_user(refresh_token=refresh_token)

    @staticmethod
    @api_router.get("/refresh_token", response_model=UserTokenResult)
    async def refresh_user_token(
        refresh_token: str,
        service=service_client,
    ) -> UserTokenResult:
        return await service.refresh_token(refresh_token=refresh_token)

    @staticmethod
    @api_router.get("/is_auth", response_model=BaseResultModel)
    async def is_auth(
        refresh_token: str,
        service=service_client,
    ) -> BaseResultModel:
        return await service.check_auth(refresh_token=refresh_token)
