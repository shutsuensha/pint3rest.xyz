"""init

Revision ID: 9b37dd31f75c
Revises: e5e3eb5de599
Create Date: 2025-04-01 18:28:03.311645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b37dd31f75c'
down_revision: Union[str, None] = 'e5e3eb5de599'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_selected_board_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'boards', ['selected_board'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.create_foreign_key('users_selected_board_fkey', 'users', 'boards', ['selected_board'], ['id'])
    # ### end Alembic commands ###
