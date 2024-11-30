from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SAnswerOption(BaseModel):
    name: str
    is_correct: bool


class SInfoAnswerOption(BaseModel):
    id: UUID
    name: str
    is_correct: bool


class SFullInfoAnswerOption(BaseModel):
    id: UUID
    name: str
    is_correct: bool
    is_selected: bool


class SQuestion(BaseModel):
    name: str
    type: str
    answers: list[SAnswerOption]


class SInfoQuestion(BaseModel):
    id: UUID
    name: str
    answers: list[SInfoAnswerOption]


class SFullInfoQuestion(BaseModel):
    id: UUID
    name: str
    # user_answer: UUID | None
    answers: list[SFullInfoAnswerOption]


class SQuiz(BaseModel):
    title: str
    description: Annotated[Optional[str], Field(default='')]
    questions: list[SQuestion]


class SInfoQuiz(BaseModel):
    id: UUID
    owner_id: UUID
    title: str
    description: Annotated[Optional[str], Field(default='')]
    created_at: datetime
    questions_count: int


class SCompletedQuiz(BaseModel):
    id: UUID
    owner_id: UUID
    title: str
    description: Annotated[Optional[str], Field(default='')]
    created_at: datetime
    correct_questions: int
    questions_count: int


class SUserAnswer(BaseModel):
    id: UUID
    quiz_id: UUID
    user_id: UUID
    question_id: UUID
    answer_id: UUID
    is_correct: bool
