from typing import Annotated

from fastapi import APIRouter, Cookie, Response, status

from app.exceptions import (UserInvalidCredentialsException,
                            UserNameAlreadyTakenException,
                            UserNotAuthenticatedException)
from app.schemas.users import SAuthUser, SEditUser

router = APIRouter(
    prefix='/users',
    tags=['auth']
)


@router.post('/register', status_code=status.HTTP_204_NO_CONTENT)
def register_user(response: Response, user: SAuthUser):
    if user.name == 'already':
        raise UserNameAlreadyTakenException
    access_token = f'access_token_{user.name}_{user.password}'
    refresh_token = f'refresh_token_{user.name}_{user.password}'
    response.set_cookie('access_token', access_token, httponly=True, max_age=120)
    response.set_cookie('refresh_token', refresh_token, httponly=True, max_age=240, path='/api/users')


@router.post('/login', status_code=status.HTTP_204_NO_CONTENT)
def login_user(response: Response, user: SAuthUser):
    if user.name == 'who' or user.password == 'invalid':
        raise UserInvalidCredentialsException
    access_token = f'access_token_{user.name}_{user.password}'
    refresh_token = f'refresh_token_{user.name}_{user.password}'
    response.set_cookie('access_token', access_token, httponly=True, max_age=120)
    response.set_cookie('refresh_token', refresh_token, httponly=True, max_age=240, path='/api/users')


@router.post('/refresh_token', status_code=status.HTTP_204_NO_CONTENT)
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
    return {'name': 'idk', 'password': 'test', 'is_teacher': True}


@router.put('/edit', status_code=status.HTTP_200_OK)
def edit_user(user: SEditUser, access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        raise UserNotAuthenticatedException
    if user == 'already':
        raise UserNameAlreadyTakenException
    return {'name': 'new idk', 'password': 'test123', 'is_teacher': False}


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        raise UserNotAuthenticatedException
