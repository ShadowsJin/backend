from datetime import datetime, timedelta, timezone
from typing import Literal, Annotated
from uuid import UUID

from fastapi import Response, Cookie
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.exceptions import (UserInvalidCredentialsException,
                            UserNameAlreadyTakenException, InvalidTokenException, UserNotAuthenticatedException)
from app.repositories.users import UsersRepository
from app.schemas.users import SUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
expiration_time = {
    'access': timedelta(minutes=30),
    'refresh': timedelta(days=30),
}


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_id_from_token(token: str) -> UUID:
    return jwt.decode(token, settings.SECRET_KEY, settings.ENCODE_ALGORITHM).get('sub')


async def check_fullname_or_email_exists(fullname: str, email: EmailStr) -> None:
    if await UsersRepository.find_one_or_none(fullname=fullname)\
            or await UsersRepository.find_one_or_none(email=email):
        raise UserNameAlreadyTakenException


def create_token(token_type: Literal['access', 'refresh'], payload: dict) -> str:
    expire = datetime.now(timezone.utc) + expiration_time[token_type]
    payload.update({'exp': expire, 'type': token_type})
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, settings.ENCODE_ALGORITHM)
    return encoded_jwt


def create_tokens_cookie(response: Response, user_id: UUID) -> None:
    access_token = create_token('access', {'sub': str(user_id)})
    refresh_token = create_token('refresh', {'sub': str(user_id)})
    response.set_cookie(
        'access_token',
        access_token,
        max_age=expiration_time['access'].seconds
    )
    response.set_cookie(
        'refresh_token',
        refresh_token,
        httponly=True,
        max_age=expiration_time['refresh'].seconds,
        path='/api/users'
    )


async def authenticate_user(email: EmailStr, password: str) -> SUser:
    user = await UsersRepository.find_one_or_none(email=email)
    if not (user and verify_password(password, user.password)):
        raise UserInvalidCredentialsException
    return user


def check_token(token: str) -> None:
    if not token:
        raise UserNotAuthenticatedException
    try:
        jwt.decode(token, settings.SECRET_KEY, settings.ENCODE_ALGORITHM)
    except JWTError:
        raise InvalidTokenException


def get_access_token(access_token: Annotated[str | None, Cookie()] = None):
    check_token(access_token)
    return access_token


def get_refresh_token(refresh_token: Annotated[str | None, Cookie()] = None):
    check_token(refresh_token)
    return refresh_token
