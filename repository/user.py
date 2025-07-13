from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.testing.pickleable import User

from models import UserProfile
from schema import UserCreateSchema


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def create_user(self, data: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(**data.model_dump()
                                           ).returning(UserProfile.id)
        async with self.db_session as session:
            user_id = (await session.execute(query)).scalar()
            await session.commit()
            return await self.get_user(user_id)

    async def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            user_profile = (await session.execute(query)).scalar_one_or_none()
            return user_profile

    async def get_user_by_name(self, username) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()






