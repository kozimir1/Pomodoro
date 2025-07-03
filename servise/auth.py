from jose import jwt, JWTError

from dataclasses import dataclass
import datetime as dt
from datetime import timedelta, timezone

from client import GoogleClient, YandexClient

from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpired, TokenNotCorrect
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema, UserCreateSchema
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def google_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.google_client.get_user_info(code)
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            print('userLogin')
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
                                            name=user_data.name,
                                            email=user_data.email,
                                            google_access_token=user_data.access_token
                                            )
        create_user = await self.user_repository.create_user(create_user_data)
        print('userCreate')
        access_token = self.generate_access_token(user_id=create_user.id)
        return UserLoginSchema(user_id=create_user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def yandex_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.yandex_client.get_user_info(code=code)
        if user := await self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            print('userLogin')
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        create_user_data = UserCreateSchema(
                                            name=user_data.name,
                                            email=user_data.default_email,
                                            yandex_access_token=user_data.access_token
                                            )
        create_user = await self.user_repository.create_user(create_user_data)
        print('userCreate')
        access_token = self.generate_access_token(user_id=create_user.id)
        return UserLoginSchema(user_id=create_user.id, access_token=access_token)

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_name(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int):
        expire_date_unix = (dt.datetime.now(timezone.utc) + timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id, 'expire': expire_date_unix},
                           self.settings.JWT_SECRET_KEY,
                           self.settings.JWT_ENCODE_ALGORITHM)
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect
        if payload['expire'] < dt.datetime.now(timezone.utc).timestamp():
            raise TokenExpired
        return payload['user_id']
