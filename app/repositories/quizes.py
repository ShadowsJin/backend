from uuid import UUID

from sqlalchemy import delete, func, insert, select, update

from app.database import async_session_maker
from app.models import Question, Quiz
from app.repositories.base import AbstractRepository
from app.schemas.quizes import SInfoQuiz


class QuizesRepository(AbstractRepository):
    @staticmethod
    async def find_one_or_none(**filter_by) -> SInfoQuiz | None:
        async with async_session_maker() as session:
            query = select(Quiz.__table__.columns, func.count(Question.id)) \
                .filter_by(**filter_by).join(Question).group_by(Quiz)
            result = await session.execute(query)
            mapping_result = result.mappings().one_or_none()
            return SInfoQuiz(
                    questions_count=mapping_result['count'],
                    **mapping_result
            ) if mapping_result else None

    @staticmethod
    async def find_all(**filter_by) -> list[SInfoQuiz]:
        async with (async_session_maker() as session):
            query = select(Quiz.__table__.columns, func.count(Question.id)) \
                .filter_by(**filter_by).join(Question).group_by(Quiz)
            result = await session.execute(query)
            mapping_result = result.mappings().all()
            return [
                SInfoQuiz(
                    questions_count=elem['count'],
                    **elem
                ) for elem in mapping_result
            ]

    @staticmethod
    async def create(**values) -> UUID:
        async with async_session_maker() as session:
            query = insert(Quiz).values(**values).returning(Quiz.id)
            quiz = await session.execute(query)
            await session.commit()
            return quiz.scalar()

    @staticmethod
    async def update(id, **values) -> None:
        async with async_session_maker() as session:
            query = update(Quiz).filter_by(id=id).values(**values).returning(Quiz.id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def delete(**filter_by) -> None:
        async with async_session_maker() as session:
            query = delete(Quiz).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
