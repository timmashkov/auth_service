from typing import List, Optional

from fastapi import Depends

from application.container import Container
from domain.user.registry import UserReadRepository, UserWriteRepository
from domain.user.schema import GetUserByUUID, UserReturnData, CreateUser, UpdateUser
from infrastructure.auth.token_handler import AuthHandler
from infrastructure.exceptions.user_exceptions import UserNotFound


class UserService:
    def __init__(
        self,
        read_repository: UserReadRepository = Depends(Container.user_read_repository),
        write_repository: UserWriteRepository = Depends(
            Container.user_write_repository,
        ),
        auth_handler: AuthHandler = Depends(Container.auth_handler),
    ):
        self.read_repo = read_repository
        self.write_repo = write_repository
        self.auth_repo = auth_handler

    async def get(self, cmd: GetUserByUUID) -> Optional[UserReturnData]:
        if result := await self.read_repo.get(user_uuid=cmd.uuid):
            return result
        raise UserNotFound

    async def get_list(self, parameter: str) -> Optional[List[UserReturnData]]:
        return await self.read_repo.get_list(parameter=parameter)

    async def create(self, data: CreateUser) -> Optional[UserReturnData]:
        _salted_pass = await self.auth_repo.encode_pass(data.password, data.login)
        return await self.write_repo.create(cmd=data)

    async def update(
        self, data: UpdateUser, user_uuid: GetUserByUUID
    ) -> Optional[UserReturnData]:
        return await self.write_repo.update(cmd=data, user_uuid=user_uuid.uuid)

    async def delete(self, user_uuid: GetUserByUUID) -> Optional[UserReturnData]:
        return await self.write_repo.delete(user_uuid=user_uuid.uuid)
