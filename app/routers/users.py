from typing import Annotated

from fastapi import APIRouter, Cookie, Response, status

from app.exceptions import (UserEmailAlreadyTakenException,
                            UserInvalidCredentialsException,
                            UserNameAlreadyTakenException,
                            UserNotAuthenticatedException)
from app.schemas.users import SFullUser, SLoginUser

router = APIRouter(
    prefix='/users',
    tags=['auth']
)


@router.post('/register', status_code=status.HTTP_204_NO_CONTENT)
def register_user(response: Response, user: SFullUser):
    if user.name == 'already':
        raise UserNameAlreadyTakenException
    if user.email == 'test@test.com':
        raise UserEmailAlreadyTakenException
    access_token = f'access_token_{user.name}_{user.password}'
    refresh_token = f'refresh_token_{user.name}_{user.password}'
    response.set_cookie('access_token', access_token, httponly=True, max_age=120)
    response.set_cookie('refresh_token', refresh_token, httponly=True, max_age=240, path='/api/users')


@router.post('/login', status_code=status.HTTP_204_NO_CONTENT)
def login_user(response: Response, user: SLoginUser):
    if user.email == 'who@you.ru' or user.password == 'invalid':
        raise UserInvalidCredentialsException
    access_token = f'access_token_{user.name}_{user.password}'
    refresh_token = f'refresh_token_{user.name}_{user.password}'
    response.set_cookie('access_token', access_token, httponly=True, max_age=120)
    response.set_cookie('refresh_token', refresh_token, httponly=True, max_age=240, path='/api/users')


@router.get('/refresh_token', status_code=status.HTTP_204_NO_CONTENT)
def refresh_user_tokens(response: Response, refresh_token: Annotated[str | None, Cookie()] = None):
    if not refresh_token:
        raise UserNotAuthenticatedException
    access_token = f'new_access_token_{refresh_token[14:]}'
    refresh_token = f'new_refresh_token_{refresh_token[14:]}'
    response.set_cookie('access_token', access_token, httponly=True, max_age=120)
    response.set_cookie('refresh_token', refresh_token, httponly=True, max_age=240, path='/api/users')


@router.get('/logout', status_code=status.HTTP_204_NO_CONTENT)
def logout_user(response: Response, refresh_token: Annotated[str | None, Cookie()] = None):
    if not refresh_token:
        raise UserNotAuthenticatedException
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')


@router.get('/me', status_code=status.HTTP_200_OK)
def get_user_data(access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        raise UserNotAuthenticatedException
    return {'name': 'idk', 'email': 'who@who.ru', 'password': 'test'}


@router.put('/edit', status_code=status.HTTP_200_OK)
def edit_user(user: SFullUser, access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        raise UserNotAuthenticatedException
    if user == 'already':
        raise UserNameAlreadyTakenException
    return {'name': 'new idk', 'email': 'hello@world.ru', 'password': 'test123'}


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        raise UserNotAuthenticatedException
