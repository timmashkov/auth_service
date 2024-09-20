from typing import Optional, List

from fastapi import Depends

from application.container import Container
from domain.user.registry import UserWriteRepository, UserReadRepository
from domain.user.schema import GetUserByUUID, UserReturnData
from infrastructure.exceptions.user_exceptions import UserNotFound


class UserService:
    def __init__(
        self,
            read_repository: UserReadRepository = Depends(Container.user_read_repository),
            write_repository: UserWriteRepository = Depends(
                Container.user_write_repository,
            )
    ):
        self.read_repo = read_repository
        self.write_repo = write_repository

    async def get_account(self, cmd: GetUserByUUID) -> Optional[UserReturnData]:
        if result := await self.read_repo.get(user_uuid=cmd.uuid):
            return result
        raise UserNotFound

    async def get_account_list(self, parameter: str) -> Optional[List[UserReturnData]]:
        return await self.read_repo.get_list(parameter=parameter)
