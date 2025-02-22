"""init

Revision ID: b8ba6b24c65e
Revises: 80fa7c2029cf
Create Date: 2025-02-22 17:40:42.367392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8ba6b24c65e'
down_revision: Union[str, None] = '80fa7c2029cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tags', 'test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('test', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
