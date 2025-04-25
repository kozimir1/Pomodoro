from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_token: str = 'a1fb50e6c86fae1679ef3351296fd6713411a08cf8dd1790a4fd05fae8688164'
    sqlite_db_name: str = 'pomodoro.sqlite'


    model_config = SettingsConfigDict(env_file='.local.env')
    '''choose token you need for your venv --.dev.env--
    .local.env -- prod.venv-- '''

