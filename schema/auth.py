from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    id: str = Field(alias='sub')
    email: str
    verified_email: bool = Field(alias="email_verified")
    name: str
    access_token: str


class YandexUserData(BaseModel):
    id: str
    login: str
    default_email: str
    name: str = Field(alias="real_name")
    access_token: str

