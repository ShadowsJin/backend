from pydantic import BaseModel, EmailStr


class SLoginUser(BaseModel):
    email: EmailStr
    password: str


class SFullUser(BaseModel):
    name: str
    email: EmailStr
    password: str
