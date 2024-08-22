from pydantic import BaseModel


class SAuthUser(BaseModel):
    name: str
    password: str


class SEditUser(BaseModel):
    name: str
    password: str
