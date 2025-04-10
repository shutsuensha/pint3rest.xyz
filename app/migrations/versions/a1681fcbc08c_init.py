"""init

Revision ID: a1681fcbc08c
Revises: c60f73d90bd8
Create Date: 2024-12-22 10:46:51.204500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1681fcbc08c'
down_revision: Union[str, None] = 'c60f73d90bd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pins', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pins', 'is_active')
    # ### end Alembic commands ###
