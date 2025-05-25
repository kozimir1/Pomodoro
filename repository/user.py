from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.testing.pickleable import User

from models import UserProfile
from schema import UserCreateSchema


@dataclass
class UserRepository:
    db_session: Session

    def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        with self.db_session() as session:
            user = session.execute(query).scalar_one_or_none()
            return user


    def create_user(self, data: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(**data.model_dump()
                                           ).returning(UserProfile.id)
        with self.db_session() as session:
            user_id = session.execute(query).scalar()
            session.commit()
            return self.get_user(user_id)

    def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session() as session:
            user_profile = session.execute(query).scalar_one_or_none()
            return user_profile

    def get_user_by_name(self, username) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()






