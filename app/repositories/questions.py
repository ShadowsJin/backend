from sqlalchemy import insert, select, update

from app.database import async_session_maker
from app.models import AnswerOption, Question
from app.repositories.base import AbstractRepository
from app.schemas.quizes import SInfoQuestion


class QuestionsRepository(AbstractRepository):
    @staticmethod
    async def find_one_or_none(**filter_by) -> SInfoQuestion | None:
        async with async_session_maker() as session:
            query = select(Question.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().one_or_none()
            if not mapping_result:
                return None
            query = select(AnswerOption.__table__.columns).filter_by(question_id=mapping_result['id'])
            answers = await session.execute(query)
            return SInfoQuestion(
                answers=answers.mappings().all(),
                **mapping_result
            )

    @staticmethod
    async def find_all(**filter_by) -> list[SInfoQuestion]:
        async with async_session_maker() as session:
            query = select(Question.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().all()
            full_result = []
            for elem in mapping_result:
                query = select(AnswerOption.__table__.columns).filter_by(question_id=elem['id'])
                answers = await session.execute(query)
                full_result.append(SInfoQuestion(
                    answers=answers.mappings().all(),
                    **elem
                ))
            return full_result

    @staticmethod
    async def create(**values) -> None:
        async with async_session_maker() as session:
            answers = values.pop('answers')
            query = insert(Question).values(**values).returning(Question.id)
            question = await session.execute(query)
            question_id = question.scalar()
            for number, answer in enumerate(answers):
                query = insert(AnswerOption).values(
                    question_id=question_id,
                    sequence_number=number,
                    **answer.model_dump()
                )
                await session.execute(query)
            await session.commit()

    @staticmethod
    async def update(id, **values) -> None:
        async with async_session_maker() as session:
            answers = values.pop('answers')
            query = update(Question).filter_by(id=id).values(**values).returning(Question.id)
            question = await session.execute(query)
            question_id = question.scalar()
            for number, answer in enumerate(answers):
                query = update(AnswerOption).filter_by(
                    question_id=question_id,
                    sequence_number=number
                ).values(**answer)
                await session.execute(query)
            await session.commit()

    @staticmethod
    async def delete(**filter_by) -> None:
        raise NotImplemented
