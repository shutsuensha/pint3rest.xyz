"""init

Revision ID: 38433812bd68
Revises: 0e8f25bf545a
Create Date: 2025-04-02 22:57:36.427250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38433812bd68'
down_revision: Union[str, None] = '0e8f25bf545a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('recommendation_created_at', sa.TIMESTAMP(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'recommendation_created_at')
    # ### end Alembic commands ###
