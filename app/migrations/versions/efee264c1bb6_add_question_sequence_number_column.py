"""add question sequence number column

Revision ID: efee264c1bb6
Revises: 1f1478f2f397
Create Date: 2024-10-13 17:35:39.510942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efee264c1bb6'
down_revision: Union[str, None] = '1f1478f2f397'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('sequence_number', sa.Integer(), autoincrement=True, nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'sequence_number')
    # ### end Alembic commands ###
