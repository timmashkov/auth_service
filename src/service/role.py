from typing import List, Optional

from fastapi import Depends

from application.container import Container
from domain.role.registry import RoleReadRepository, RoleWriteRepository
from domain.role.schema import CreateRole, GetRoleByUUID, RoleReturnData


class UserService:
    def __init__(
        self,
        read_repository: RoleReadRepository = Depends(Container.role_read_repository),
        write_repository: RoleWriteRepository = Depends(
            Container.role_write_repository,
        ),
    ):
        self.read_repo = read_repository
        self.write_repo = write_repository

    async def get(self, cmd: GetRoleByUUID) -> Optional[RoleReturnData]:
        raise await self.read_repo.get(user_uuid=cmd.uuid)

    async def get_list(self, parameter: str) -> Optional[List[RoleReturnData]]:
        return await self.read_repo.get_list(parameter=parameter)

    async def create(self, data: CreateRole) -> Optional[RoleReturnData]:

        return await self.write_repo.create(cmd=data)

    async def update(
        self, data: CreateRole, user_uuid: GetRoleByUUID
    ) -> Optional[RoleReturnData]:
        return await self.write_repo.update(cmd=data, user_uuid=user_uuid.uuid)

    async def delete(self, user_uuid: GetRoleByUUID) -> Optional[RoleReturnData]:
        return await self.write_repo.delete(user_uuid=user_uuid.uuid)
