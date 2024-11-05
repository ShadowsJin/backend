from uuid import UUID

from fastapi import APIRouter, Depends, status, Query

from app.exceptions import (QuestionNotFoundException, QuizNotFoundException,
                            QuizOwnerException, QuizTitleAlreadyTakenException)
from app.repositories.answers import AnswersRepository
from app.repositories.questions import QuestionsRepository
from app.repositories.quizes import QuizesRepository
from app.schemas.quizes import SQuiz, SFullInfoQuestion, SInfoQuestion, SFullInfoAnswerOption
from app.utils import get_access_token, get_user_id_from_token

router = APIRouter(
    prefix='/quizes',
    tags=['quizes']
)


@router.get('/created', status_code=status.HTTP_200_OK)
async def get_created_quizes(access_token: str = Depends(get_access_token)):
    user_id = get_user_id_from_token(access_token)
    return await QuizesRepository.find_all(owner_id=user_id)


@router.get('/completed', status_code=status.HTTP_200_OK)
async def get_completed_quizes(access_token: str = Depends(get_access_token)):
    user_id = get_user_id_from_token(access_token)
    completed_quizes = await AnswersRepository.find_all(user_id=user_id)
    return [await QuizesRepository.find_one_or_none(id=quiz.quiz_id) for quiz in completed_quizes]


@router.post('/new', status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz: SQuiz, access_token: str = Depends(get_access_token)):
    user_id = get_user_id_from_token(access_token)
    if await QuizesRepository.find_one_or_none(title=quiz.title):
        raise QuizTitleAlreadyTakenException
    quiz_id = await QuizesRepository.create(
        title=quiz.title,
        description=quiz.description,
        owner_id=user_id
    )
    for number, question in enumerate(quiz.questions):
        await QuestionsRepository.create(
            name=question.name,
            sequence_number=number,
            quiz_id=quiz_id,
            answers=question.answers
        )
    return quiz_id


@router.get('/{quiz_id}', status_code=status.HTTP_200_OK)
async def get_quiz(quiz_id: UUID, access_token: str = Depends(get_access_token)):
    quiz = await QuizesRepository.find_one_or_none(id=quiz_id)
    if not quiz:
        raise QuizNotFoundException
    return quiz


@router.get('/{quiz_id}/questions', status_code=status.HTTP_200_OK)
async def get_quiz_questions(quiz_id: UUID, access_token: str = Depends(get_access_token)):
    quiz = await QuizesRepository.find_one_or_none(id=quiz_id)
    if not quiz:
        raise QuizNotFoundException
    questions = await QuestionsRepository.find_all(quiz_id=quiz_id)
    return questions


@router.post('/send_answer/{quiz_id}/{question_no}', status_code=status.HTTP_204_NO_CONTENT)
async def send_answer(
        quiz_id: UUID,
        question_no: int,
        answer: list[UUID] = Query(),
        access_token: str = Depends(get_access_token)
):
    user_id = get_user_id_from_token(access_token)
    quiz = await QuizesRepository.find_one_or_none(id=quiz_id)
    if not quiz:
        raise QuizNotFoundException
    question = await QuestionsRepository.find_one_or_none(quiz_id=quiz_id, sequence_number=question_no)
    if not question:
        raise QuestionNotFoundException
    await AnswersRepository.delete(
        quiz_id=quiz_id,
        question_id=question.id,
        user_id=user_id
    )
    for ans in answer:
        await AnswersRepository.create(
            quiz_id=quiz_id,
            question_id=question.id,
            user_id=user_id,
            answer_id=ans
        )


@router.get('/finish_test/{quiz_id}', status_code=status.HTTP_200_OK)
async def finish_test(quiz_id: UUID, access_token: str = Depends(get_access_token)):
    user_id = get_user_id_from_token(access_token)
    quiz = await QuizesRepository.find_one_or_none(id=quiz_id)
    if not quiz:
        raise QuizNotFoundException
    user_answers = await AnswersRepository.find_all(
        quiz_id=quiz_id,
        user_id=user_id
    )
    for number, user_answer in enumerate(user_answers):
        question = await QuestionsRepository.find_one_or_none(id=user_answer.question_id)
        correct_answers_ids = [answer.id for answer in question.answers if answer.is_correct]
        if user_answer.answer_id in correct_answers_ids:
            await AnswersRepository.update(
                id=user_answer.id,
                quiz_id=quiz_id,
                user_id=user_id,
                question_id=question.id,
                answer_id=user_answer.answer_id,
                is_correct=True
            )
    user_answers = await AnswersRepository.find_all(
        quiz_id=quiz_id,
        user_id=user_id,
        is_correct=True
    )
    return {'correct': len(user_answers), 'total': quiz.questions_count}


@router.get('/{quiz_id}/{question_no}', status_code=status.HTTP_200_OK)
async def get_quiz_question(quiz_id: UUID, question_no: int, access_token: str = Depends(get_access_token)):
    user_id = get_user_id_from_token(access_token)
    quiz = await QuizesRepository.find_one_or_none(id=quiz_id)
    if not quiz:
        raise QuizNotFoundException
    question = await QuestionsRepository.find_one_or_none(quiz_id=quiz_id, sequence_number=question_no)
    if not question:
        raise QuestionNotFoundException
    user_answer = await AnswersRepository.find_all(
        quiz_id=quiz_id,
        question_id=question.id,
        user_id=user_id
    )
    user_answer_ids = [answer.answer_id for answer in user_answer]
    return SFullInfoQuestion(
        id=question.id,
        name=question.name,
        answers=[
            SFullInfoAnswerOption(
                is_selected=(answer.id in user_answer_ids),
                **answer.model_dump()
            ) for answer in question.answers
        ]
    )


@router.put('/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
async def edit_quiz(quiz_id: UUID, quiz: SQuiz, access_token: str = Depends(get_access_token)):
    old_quiz = await QuizesRepository.find_one_or_none(id=quiz_id)
    user_id = get_user_id_from_token(access_token)
    if not old_quiz:
        raise QuizNotFoundException
    if str(old_quiz.owner_id) != user_id:
        raise QuizOwnerException
    await QuizesRepository.update(
        id=old_quiz.id,
        title=quiz.title,
        description=quiz.description,
        owner_id=user_id
    )
    for number, question in enumerate(quiz.questions):
        question_id = QuestionsRepository.find_one_or_none(
            quiz_id=quiz_id,
            sequence_number=number
        )
        await QuestionsRepository.update(
            id=question_id,
            name=question.name
        )
        for number, answer in enumerate(question.answers):
            answer_option_id = QuestionsRepository.find_one_or_none(
                question_id=question_id,
                sequence_number=number
            )
            await AnswersRepository.update(
                id=answer_option_id,
                name=answer.name,
                is_corrent=answer.is_correct,
            )
    return quiz_id


@router.delete('/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(quiz_id: UUID, access_token: str = Depends(get_access_token)):
    quiz = await QuizesRepository.find_one_or_none(id=quiz_id)
    if not quiz:
        raise QuizNotFoundException
    if str(quiz.owner_id) != get_user_id_from_token(access_token):
        raise QuizOwnerException
    await QuizesRepository.delete(id=quiz_id)
