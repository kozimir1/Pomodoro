from dataclasses import dataclass

from repository import UserRepository
from schema import UserLoginSchema, UserCreateSchema
from servise.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        user_create_schema = UserCreateSchema(username=username, password=password)
        user = await self.user_repository.create_user(user_create_schema)
        access_token = self.auth_service.generate_access_token(user.id)
        return UserLoginSchema(user_id=user.id,
                               access_token=access_token)




