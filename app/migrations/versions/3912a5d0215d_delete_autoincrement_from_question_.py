"""delete autoincrement from question sequence number (dont work)

Revision ID: 3912a5d0215d
Revises: 8130bf49d298
Create Date: 2024-10-13 19:06:31.015918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3912a5d0215d'
down_revision: Union[str, None] = '8130bf49d298'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###