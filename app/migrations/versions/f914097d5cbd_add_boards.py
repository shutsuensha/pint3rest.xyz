"""add boards

Revision ID: f914097d5cbd
Revises: 9cab031ee01e
Create Date: 2025-04-01 01:14:05.752809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f914097d5cbd'
down_revision: Union[str, None] = '9cab031ee01e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('boards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('board_pins',
    sa.Column('board_id', sa.Integer(), nullable=False),
    sa.Column('pin_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['pin_id'], ['pins.id'], ),
    sa.PrimaryKeyConstraint('board_id', 'pin_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('board_pins')
    op.drop_table('boards')
    # ### end Alembic commands ###
