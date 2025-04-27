from dataclasses import dataclass

from models import UserProfile


@dataclass
class UserRepository:

    def create_user(self, username: str, password: str) -> UserProfile:
        pass
