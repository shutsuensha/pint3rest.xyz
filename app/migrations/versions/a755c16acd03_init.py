"""init

Revision ID: a755c16acd03
Revises: fb4bb5258e24
Create Date: 2025-04-04 23:37:03.081098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a755c16acd03'
down_revision: Union[str, None] = 'fb4bb5258e24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('updates', 'update_type',
               existing_type=postgresql.ENUM('recommendations', 'follow', 'like_pin', 'save_pin', 'comment_pin', 'like_comment', 'reply_comment', name='update_type_enum'),
               type_=sa.String(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('updates', 'update_type',
               existing_type=sa.String(length=100),
               type_=postgresql.ENUM('recommendations', 'follow', 'like_pin', 'save_pin', 'comment_pin', 'like_comment', 'reply_comment', name='update_type_enum'),
               existing_nullable=False)
    # ### end Alembic commands ###
