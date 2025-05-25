from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserProfile(Base):
    __tablename__ = 'UserProfile'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    google_access_token: Mapped[str] = mapped_column(nullable=True)


