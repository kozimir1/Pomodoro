from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    id: str = Field(alias='sub')
    email: str
    verified_email: bool = Field(alias="email_verified")
    name: str
    access_token: str
