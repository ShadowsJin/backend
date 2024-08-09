from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

MAX_TEXT_LENGTH = 150
unique_name = Annotated[str, mapped_column(String(MAX_TEXT_LENGTH), unique=True)]


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
