from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from settings import Settings

engine = create_async_engine(url=Settings().db_url, future=True, echo=True, pool_pre_ping=True)

# 'sqlite:///pomodoro.sqlite'

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session

