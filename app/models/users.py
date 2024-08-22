from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models.base import MAX_TEXT_LENGTH, UUIDMixin, unique_name


class User(UUIDMixin, Base):
    __tablename__ = 'users'

    fullname: Mapped[unique_name]
    email: Mapped[unique_name]
    password: Mapped[str] = mapped_column(String(MAX_TEXT_LENGTH))
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    created_quizes: Mapped[list['Quiz']] = relationship(back_populates='owner')
