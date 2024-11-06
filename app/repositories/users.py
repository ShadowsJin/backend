from uuid import UUID

from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker
from app.models.users import User
from app.repositories.base import AbstractRepository
from app.schemas.users import SInfoUser, SUser


class UsersRepository(AbstractRepository):
    @staticmethod
    async def find_all(**filter_by):
        raise NotImplementedError

    @staticmethod
    async def find_one_or_none(**filter_by) -> SUser:
        async with async_session_maker() as session:
            query = select(User.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().one_or_none()
            return SUser(**mapping_result) if mapping_result else None

    @staticmethod
    async def create(**values) -> UUID:
        async with async_session_maker() as session:
            query = insert(User).values(**values).returning(User.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @staticmethod
    async def update(id, **values) -> SInfoUser:
        async with async_session_maker() as session:
            query = update(User).filter_by(id=id).values(**values).returning(User.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            mapping_result = result.mappings().one_or_none()
            return SInfoUser(**mapping_result) if mapping_result else None

    @staticmethod
    async def delete(**filter_by) -> None:
        async with async_session_maker() as session:
            query = delete(User).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
