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
    auth_token = f'token_{user.name}_{user.password}'
    response.set_cookie('auth_token', auth_token, httponly=True, max_age=120)


@router.post('/login', status_code=status.HTTP_204_NO_CONTENT)
def login_user(response: Response, user: SAuthUser):
    if user.name == 'who' or user.password == 'invalid':
        raise UserInvalidCredentialsException
    auth_token = f'token_{user.name}_{user.password}'
    response.set_cookie('auth_token', auth_token, httponly=True, max_age=120)


@router.get('/logout', status_code=status.HTTP_204_NO_CONTENT)
def logout_user(response: Response, auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    response.delete_cookie('auth_token')


@router.get('/me', status_code=status.HTTP_200_OK)
def get_user_data(auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    return {'name': 'idk', 'password': 'test', 'is_teacher': True}


@router.put('/edit', status_code=status.HTTP_200_OK)
def edit_user(user: SEditUser, auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    if user == 'already':
        raise UserNameAlreadyTakenException
    return {'name': 'new idk', 'password': 'test123', 'is_teacher': False}


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
