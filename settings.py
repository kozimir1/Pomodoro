from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_token: str = 'a1fb50e6c86fae1679ef3351296fd6713411a08cf8dd1790a4fd05fae8688164'

    DB_HOST: str = '0.0.0.0'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'pomodoro'
    DB_DRIVER: str = 'postgresql+psycopg2'

    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    JWT_SECRET_KEY: str = 'sekret-key'
    JWT_ENCODE_ALGORITHM: str = 'HS256'

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


    sqlite_db_name: str = 'pomodoro.sqlite'


    model_config = SettingsConfigDict(env_file='.local.env')
    '''choose token you need for your venv --.dev.env--
    .local.env -- prod.venv-- '''

