"""init

Revision ID: 8587cf163ef5
Revises: 7f368f144b4c
Create Date: 2025-01-01 00:44:16.906766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8587cf163ef5'
down_revision: Union[str, None] = '7f368f144b4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pins', sa.Column('height', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pins', 'height')
    # ### end Alembic commands ###
