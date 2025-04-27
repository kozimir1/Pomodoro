from dataclasses import dataclass

from repository import UserRepository
from schema import UserLoginSchema


@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.create_user(username, password)
        return UserLoginSchema(username=user.id, access_token=user.access_token)
