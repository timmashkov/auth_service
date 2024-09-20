from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from domain.user.schema import UserReturnData, GetUserByUUID
from service.user import UserService


class UserRouter:
    api_router = APIRouter(prefix="/user", tags=["User"])

    @staticmethod
    @api_router.get("/one", response_model=UserReturnData)
    async def show_user(
        user_uuid: str | UUID,
        account_registry: UserService = Depends(UserService),
    ) -> UserReturnData:
        return await account_registry.get_account(cmd=GetUserByUUID(uuid=user_uuid))

    @staticmethod
    @api_router.get("/all", response_model=List[UserReturnData])
    async def get_users(
        parameter: str = "created_at",
        account_registry: UserService = Depends(UserService),
    ) -> List[UserReturnData]:
        return await account_registry.get_account_list(parameter=parameter)
