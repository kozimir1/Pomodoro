from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import Settings

settings = Settings()
engine = create_engine(settings.db_url)

# 'sqlite:///pomodoro.sqlite'

Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session
