from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    username: str
    access_token: str
