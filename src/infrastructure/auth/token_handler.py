import hashlib
from datetime import datetime
from uuid import UUID

import jwt
from fastapi.security import APIKeyHeader, HTTPBearer

from infrastructure.exceptions.token_exceptions import (
    InvalidRefreshToken,
    InvalidScopeToken,
    InvalidToken,
    RefreshTokenExpired,
    TokenExpired,
)


class AuthHandler:
    def __init__(
        self,
        secret: str,
        exp: int,
        api_x_key_header: str,
        iterations: int,
        hash_name: str,
        formats: str,
        algorythm: str,
    ):
        self._secret = secret
        self._exp = exp
        self._api_x_key_header = APIKeyHeader(name=api_x_key_header)
        self._iterations = iterations
        self._hash_name = hash_name
        self._formats = formats
        self._algorythm = algorythm
        self._jwt_header = HTTPBearer()

    async def encode_pass(self, password: str, salt: str) -> str:
        password = password.encode(self._formats)
        salt = salt.encode(self._formats)
        hashed_pass = hashlib.pbkdf2_hmac(
            self._hash_name,
            password=password,
            salt=salt,
            iterations=self._iterations,
        )
        return hashed_pass.hex()

    async def verify_password(
        self,
        password: str,
        salt: str,
        encoded_pass: str,
    ) -> bool:
        hashed_password = await self.encode_pass(password=password, salt=salt)
        return hashed_password == encoded_pass

    async def encode_token(self, user_id: UUID) -> str:
        expiration = self._exp
        timestamp = datetime.now().timestamp()
        payload = {
            "expiration": int(timestamp + expiration),
            "iat": int(timestamp),
            "scope": "access_token",
            "sub": str(user_id),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorythm)

    async def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorythm])
            if payload["scope"] == "refresh_token":
                return payload["sub"]
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise TokenExpired
        except jwt.InvalidTokenError:
            raise InvalidToken

    async def encode_refresh_token(self, user_id: UUID | str) -> str:
        expiration = self._exp
        timestamp = datetime.now().timestamp()
        payload = {
            "expiration": int(timestamp + expiration),
            "iat": int(timestamp),
            "scope": "refresh_token",
            "sub": str(user_id),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorythm)

    async def decode_refresh_token(self, token: str) -> str:
        payload = jwt.decode(token, self._secret, algorithms=[self._algorythm])
        if payload["scope"] == "refresh_token":
            return payload["sub"]
        raise InvalidScopeToken

    async def refresh_token(self, refresh_token: str) -> dict[str, str]:
        try:
            payload = jwt.decode(
                refresh_token,
                self._secret,
                algorithms=[self._algorythm],
            )
            if payload["scope"] == "refresh_token":
                user_id = payload["sub"]
                new_token = await self.encode_token(user_id)
                new_refresh = await self.encode_refresh_token(user_id)
                return {"new_access_token": new_token, "new_refresh_token": new_refresh}
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise RefreshTokenExpired
        except jwt.InvalidTokenError:
            raise InvalidRefreshToken
