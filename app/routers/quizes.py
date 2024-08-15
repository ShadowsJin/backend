from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Cookie, status

from app.exceptions import (AnswerNotFoundException, QuizNotFoundException,
                            QuizOwnerException, UserNotAuthenticatedException)
from app.schemas.quizes import SQuiz

router = APIRouter(
    prefix='/quizes',
    tags=['quizes']
)


@router.get('/created', status_code=status.HTTP_200_OK)
def get_created_quizes(auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    return [
        {'id': '32da9f82-aece-4f9f-b70b-99adc6389798', 'name': 'Тест1'},
        {'id': '9f1b697a-093c-43ba-8801-755e27115fd5', 'name': 'Тест2'}
    ]


@router.get('/completed', status_code=status.HTTP_200_OK)
def get_completed_quizes(auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    return [
        {'id': '42d9fcbc-4732-4662-80d5-f8f42b874ffc', 'name': 'Тест3', 'correct': 5, 'total': 5},
        {'id': '3fe90d70-3287-4f86-99dd-bf68e96febbf', 'name': 'Тест4', 'correct': 3, 'total': 7}
    ]


@router.post('/new', status_code=status.HTTP_201_CREATED)
def create_quiz(quiz: SQuiz, auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    return {'id': 'e2ae7f46-660f-47f4-be38-d8998fb9bf21'}


@router.get('/{quiz_id}', status_code=status.HTTP_200_OK)
def get_quiz(quiz_id: UUID, auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    if quiz_id == 'a326a03c-68d3-4b27-9fcc-3350e9251846':
        raise QuizNotFoundException
    return {'name': 'Тестовый тест', 'description': 'Что происходит..', 'owner': 'who??'}


@router.get('/{quiz_id}/{question_no}', status_code=status.HTTP_200_OK)
def get_quiz_question(quiz_id: UUID, question_no: int, auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    if quiz_id == 'a326a03c-68d3-4b27-9fcc-3350e9251846':
        raise QuizNotFoundException
    if question_no == 3:
        raise AnswerNotFoundException
    return {
        'name': 'Что такое земля?',
        'type': 1,
        'answers': [
            {'name': 'планета', 'is_correct': True},
            {'name': 'то, что под ногами', 'is_correct': True},
            {'name': 'помогите.. я пишу это в 2:33 ночи', 'is_correct': False}
        ]
    }


@router.post('/send_answer/{quiz_id}/{question_no}', status_code=status.HTTP_204_NO_CONTENT)
def send_answer(quiz_id: UUID, question_no: int, answer: str | UUID, auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    if quiz_id == 'a326a03c-68d3-4b27-9fcc-3350e9251846':
        raise QuizNotFoundException
    if question_no == 3:
        raise AnswerNotFoundException


@router.get('/finish_test/{quiz_id}', status_code=status.HTTP_200_OK)
def finish_test(quiz_id: UUID, auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    if quiz_id == 'a326a03c-68d3-4b27-9fcc-3350e9251846':
        raise QuizNotFoundException
    return {'correct': 3, 'total': 4}


@router.put('/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
def edit_quiz(quiz_id: UUID, quiz: SQuiz, auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    if auth_token == 'token_123_123':
        raise QuizOwnerException
    if quiz_id == 'a326a03c-68d3-4b27-9fcc-3350e9251846':
        raise QuizNotFoundException


@router.delete('/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(quiz_id: UUID, auth_token: Annotated[str | None, Cookie()] = None):
    if not auth_token:
        raise UserNotAuthenticatedException
    if auth_token == 'token_123_123':
        raise QuizOwnerException
    if quiz_id == 'a326a03c-68d3-4b27-9fcc-3350e9251846':
        raise QuizNotFoundException
