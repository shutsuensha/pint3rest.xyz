"""init

Revision ID: e29bf9954e2b
Revises: f7c225088ee5
Create Date: 2025-01-14 04:02:32.824902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e29bf9954e2b'
down_revision: Union[str, None] = 'f7c225088ee5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('description', sa.String(length=400), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'description')
    # ### end Alembic commands ###
