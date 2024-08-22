from pydantic import BaseModel, EmailStr


class SLoginUser(BaseModel):
    email: EmailStr
    password: str


class SFullUser(BaseModel):
    fullname: str
    email: EmailStr
    password: str
