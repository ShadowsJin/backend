from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response, status
from jose import jwt
from jose.exceptions import JWTError

from app.config import settings
from app.exceptions import InvalidTokenException, UserNotAuthenticatedException
from app.repositories.users import UsersRepository
from app.schemas.users import SInfoUser, SLoginUser, SRegisterUser
from app.utils import (authenticate_user, check_fullname_or_email_exists,
                       create_tokens_cookie, get_password_hash,
                       get_user_id_from_token)

router = APIRouter(
    prefix='/users',
    tags=['auth']
)


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


@router.post('/register', status_code=status.HTTP_204_NO_CONTENT)
async def register_user(response: Response, user: SRegisterUser):
    await check_fullname_or_email_exists(user.fullname, user.email)
    new_user_id = await UsersRepository.create(
        fullname=user.fullname,
        email=user.email,
        password=get_password_hash(user.password),
    )
    create_tokens_cookie(response, new_user_id)


@router.post('/login', status_code=status.HTTP_204_NO_CONTENT)
async def login_user(response: Response, user: SLoginUser):
    user = await authenticate_user(user.email, user.password)
    create_tokens_cookie(response, user.id)


@router.get('/refresh_token', status_code=status.HTTP_204_NO_CONTENT)
def refresh_user_tokens(response: Response, refresh_token: str = Depends(get_refresh_token)):
    user_id = get_user_id_from_token(refresh_token)
    create_tokens_cookie(response, user_id)


@router.get('/logout', status_code=status.HTTP_204_NO_CONTENT)
def logout_user(response: Response, refresh_token: str = Depends(get_refresh_token)):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')


@router.get('/me', status_code=status.HTTP_200_OK)
async def get_user_data(access_token: str = Depends(get_access_token)):
    user_id = get_user_id_from_token(access_token)
    user = await UsersRepository.find_one_or_none(id=user_id)
    return SInfoUser(**user.model_dump())


@router.put('/edit', status_code=status.HTTP_200_OK)
async def edit_user(user: SRegisterUser, access_token: str = Depends(get_access_token)):
    user_id = get_user_id_from_token(access_token)
    await check_fullname_or_email_exists(user.fullname, user.email)
    return await UsersRepository.update(
        id=user_id,
        fullname=user.fullname,
        email=user.email,
        password=get_password_hash(user.password),
    )


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(response: Response, access_token: str = Depends(get_access_token)):
    user_id = get_user_id_from_token(access_token)
    await UsersRepository.delete(id=user_id)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
