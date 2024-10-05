from typing import List, Optional

from fastapi import Depends

from application.container import Container
from domain.permission.registry import (
    PermissionReadRepository,
    PermissionWriteRepository,
)
from domain.permission.schema import (
    CreatePermission,
    GetPermissionByUUID,
    PermissionReturnData,
)


class PermissionService:
    def __init__(
        self,
        read_repository: PermissionReadRepository = Depends(
            Container.perm_read_repository
        ),
        write_repository: PermissionWriteRepository = Depends(
            Container.perm_write_repository,
        ),
    ):
        self.read_repo = read_repository
        self.write_repo = write_repository

    async def get(self, cmd: GetPermissionByUUID) -> Optional[PermissionReturnData]:
        raise await self.read_repo.get(perm_uuid=cmd.uuid)

    async def get_list(self, parameter: str) -> Optional[List[PermissionReturnData]]:
        return await self.read_repo.get_list(parameter=parameter)

    async def create(self, data: CreatePermission) -> Optional[PermissionReturnData]:

        return await self.write_repo.create(cmd=data)

    async def update(
        self, data: CreatePermission, perm_uuid: GetPermissionByUUID
    ) -> Optional[PermissionReturnData]:
        return await self.write_repo.update(cmd=data, perm_uuid=perm_uuid.uuid)

    async def delete(
        self, perm_uuid: GetPermissionByUUID
    ) -> Optional[PermissionReturnData]:
        return await self.write_repo.delete(perm_uuid=perm_uuid.uuid)
