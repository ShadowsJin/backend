"""add question_id column to answer_options table

Revision ID: 148c792d2c41
Revises: 3912a5d0215d
Create Date: 2024-10-13 19:14:34.442447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '148c792d2c41'
down_revision: Union[str, None] = '3912a5d0215d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer_options', sa.Column('question_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'answer_options', 'questions', ['question_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'answer_options', type_='foreignkey')
    op.drop_column('answer_options', 'question_id')
    # ### end Alembic commands ###