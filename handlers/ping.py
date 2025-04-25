from fastapi import APIRouter
from settings import Settings

router = APIRouter(prefix='/ping', tags=['ping'])


@router.get('/db')
def ping_db():
    settings = Settings()
    return {'message': (settings.google_token, settings.sqlite_db_name)}


@router.get('/app')
def ping_app():
    return {'message': 'app is fine'}
