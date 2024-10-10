from uuid import UUID

from pydantic import BaseModel, EmailStr


class SLoginUser(BaseModel):
    email: EmailStr
    password: str


class SInfoUser(BaseModel):
    fullname: str
    email: EmailStr


class SRegisterUser(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class SUser(BaseModel):
    id: UUID
    fullname: str
    email: EmailStr
    password: str
