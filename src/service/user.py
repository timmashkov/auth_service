import asyncio
from typing import List, Optional

from fastapi import Depends

from application.config import settings
from application.container import Container
from domain.user.registry import UserReadRepository, UserWriteRepository
from domain.user.schema import (
    CreateUser,
    GetUserByUUID,
    LoginUser,
    UpdateUser,
    UserReturnData,
    UserTokenResult,
)
from infrastructure.auth.token_handler import AuthHandler
from infrastructure.base_entities.base_model import BaseResultModel
from infrastructure.broker.kafka import KafkaProducer
from infrastructure.exceptions.token_exceptions import Unauthorized
from infrastructure.exceptions.user_exceptions import UserNotFound, WrongPassword


class UserService:
    def __init__(
        self,
        read_repository: UserReadRepository = Depends(Container.user_read_repository),
        write_repository: UserWriteRepository = Depends(
            Container.user_write_repository,
        ),
        auth_handler: AuthHandler = Depends(Container.auth_handler),
        kafka_handler: KafkaProducer = Depends(Container.producer_client),
    ):
        self.read_repo = read_repository
        self.write_repo = write_repository
        self.auth_repo = auth_handler
        self.kafka_repo = kafka_handler

    async def get(self, cmd: GetUserByUUID) -> Optional[UserReturnData]:
        if result := await self.read_repo.get(user_uuid=cmd.uuid):
            return result
        raise UserNotFound

    async def get_list(self, parameter: str) -> Optional[List[UserReturnData]]:
        return await self.read_repo.get_list(parameter=parameter)

    async def create(self, data: CreateUser) -> Optional[UserReturnData]:
        _salted_pass = await self.auth_repo.encode_pass(data.password, data.login)
        cmd = CreateUser(
            login=data.login,
            password=_salted_pass,
            email=data.email,
            phone_number=data.phone_number,
            age=data.age,
        )
        if created_user := await self.write_repo.create(cmd=cmd):
            data_dict = cmd.model_dump()
            data_dict["user_uuid"] = str(created_user.uuid)
            data_dict["event_type"] = "create"
            asyncio.create_task(
                self.kafka_repo.send_message(
                    message=data_dict,
                ),
            )
        return created_user

    async def update(
        self, data: UpdateUser, user_uuid: GetUserByUUID
    ) -> Optional[UserReturnData]:
        if updated_user := await self.write_repo.update(
            cmd=data, user_uuid=user_uuid.uuid
        ):
            data_dict = data.model_dump()
            data_dict["user_uuid"] = str(updated_user.uuid)
            data_dict["event_type"] = "update"
            asyncio.create_task(
                self.kafka_repo.send_message(
                    message=data_dict,
                ),
            )
        return updated_user

    async def delete(self, user_uuid: GetUserByUUID) -> Optional[UserReturnData]:
        if deleted_user := await self.write_repo.delete(user_uuid=user_uuid.uuid):
            data_dict = {"user_uuid": str(deleted_user.uuid), "event_type": "delete"}
            asyncio.create_task(
                self.kafka_repo.send_message(
                    message=data_dict,
                ),
            )
        return deleted_user

    async def login_user(self, cmd: LoginUser) -> UserTokenResult:
        user = await self.read_repo.get_by_login(login=cmd.login)
        if not user:
            raise UserNotFound
        if not await self.auth_repo.verify_password(
            password=cmd.password,
            salt=cmd.login,
            encoded_pass=user.password,
        ):
            raise WrongPassword
        access_token = await self.auth_repo.encode_token(user_id=user.uuid)
        refresh_token = await self.auth_repo.encode_refresh_token(user_id=user.uuid)
        await self.auth_repo.save_tokens_to_session(
            access_token=access_token,
            refresh_token=refresh_token,
            user_uuid=str(user.uuid),
        )
        return UserTokenResult(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def logout_user(self, refresh_token: str) -> BaseResultModel:
        user_uuid = await self.auth_repo.decode_refresh_token(token=refresh_token)
        tokens = await self.auth_repo.get_tokens_from_session(user_uuid=user_uuid)
        if not tokens:
            raise Unauthorized
        if tokens["refresh_token"] == refresh_token:
            await self.auth_repo.del_tokes_from_session(user_uuid=user_uuid)
            return BaseResultModel(status=True)
        raise Unauthorized

    async def refresh_token(self, refresh_token: str) -> UserTokenResult:
        user_uuid = await self.auth_repo.decode_refresh_token(token=refresh_token)
        tokens = await self.auth_repo.get_tokens_from_session(user_uuid=user_uuid)
        if not tokens:
            raise Unauthorized
        if tokens["refresh_token"] == refresh_token:
            new_tokens = await self.auth_repo.refresh_token(refresh_token=refresh_token)
            await self.auth_repo.save_tokens_to_session(
                access_token=new_tokens["new_access_token"],
                refresh_token=new_tokens["new_refresh_token"],
                user_uuid=user_uuid,
            )
            return UserTokenResult(
                access_token=new_tokens["new_access_token"],
                refresh_token=new_tokens["new_refresh_token"],
            )
        raise Unauthorized

    async def check_auth(self, refresh_token: str) -> BaseResultModel:
        user_uuid = await self.auth_repo.decode_refresh_token(token=refresh_token)
        tokens = await self.auth_repo.get_tokens_from_session(user_uuid=user_uuid)
        if not tokens:
            raise Unauthorized
        if tokens["refresh_token"] == refresh_token:
            return BaseResultModel(status=True)
        raise Unauthorized
