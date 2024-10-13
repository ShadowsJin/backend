from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models.base import MAX_TEXT_LENGTH, UUIDMixin, unique_name

MAX_QUESTION_LENGTH = 500


class Quiz(UUIDMixin, Base):
    __tablename__ = 'quizes'

    title: Mapped[unique_name]
    description: Mapped[Optional[str]] = mapped_column(String(MAX_QUESTION_LENGTH))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    owner: Mapped['User'] = relationship(back_populates='created_quizes')
    questions: Mapped[list['Question']] = relationship(back_populates='quiz')


class Question(UUIDMixin, Base):
    __tablename__ = 'questions'

    name: Mapped[str] = mapped_column(String(MAX_QUESTION_LENGTH))
    sequence_number: Mapped[int]

    quiz_id: Mapped[UUID] = mapped_column(
        ForeignKey('quizes.id', ondelete='CASCADE')
    )
    quiz: Mapped['Quiz'] = relationship(back_populates='questions')


class AnswerOption(UUIDMixin, Base):
    __tablename__ = 'answer_options'

    name: Mapped[str] = mapped_column(String(MAX_TEXT_LENGTH))
    is_correct: Mapped[bool]


class UserAnswer(UUIDMixin, Base):
    __tablename__ = 'user_answers'

    answer: Mapped[UUID]
    is_correct: Mapped[bool]

    quiz_id: Mapped[UUID] = mapped_column(
        ForeignKey('quizes.id', ondelete='CASCADE')
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    question_id: Mapped[UUID] = mapped_column(
        ForeignKey('questions.id', ondelete='CASCADE')
    )
    answer_id: Mapped[UUID] = mapped_column(
        ForeignKey('answer_options.id', ondelete='CASCADE')
    )
    quiz: Mapped['Quiz'] = relationship()
    user: Mapped['User'] = relationship()
    question: Mapped['Question'] = relationship()
    answer: Mapped['AnswerOption'] = relationship()

    UniqueConstraint("quiz_id", "user_id", "question_id")
