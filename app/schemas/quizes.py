from typing import Optional

from pydantic import BaseModel


class SAnswerOption(BaseModel):
    name: str
    is_correct: bool


class SQuestion(BaseModel):
    name: str
    type: int
    answers: Optional[list[SAnswerOption]]


class SQuiz(BaseModel):
    name: str
    description: Optional[str]
    questions: list[SQuestion]
