from uuid import UUID

from sqlalchemy import insert, select, update

from app.database import async_session_maker
from app.models import AnswerOption, UserAnswer
from app.repositories.base import AbstractRepository
from app.schemas.quizes import SUserAnswer


class AnswersRepository(AbstractRepository):
    @staticmethod
    async def find_one_or_none(**filter_by) -> SUserAnswer | None:
        async with async_session_maker() as session:
            query = select(UserAnswer.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().one_or_none()
            return SUserAnswer(**mapping_result) if mapping_result else None

    @staticmethod
    async def find_all(**filter_by) -> list[SUserAnswer]:
        async with async_session_maker() as session:
            query = select(UserAnswer.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().all()
            return [SUserAnswer(**elem) for elem in mapping_result] if mapping_result else []

    @staticmethod
    async def create(**values) -> None:
        async with async_session_maker() as session:
            query = insert(UserAnswer).values(**values)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def update(id, **values) -> None:
        async with async_session_maker() as session:
            query = update(UserAnswer).filter_by(id=id).values(**values)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def delete(**filter_by) -> None:
        raise NotImplementedError
