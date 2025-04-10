"""init

Revision ID: 11a1166a9bef
Revises: 8587cf163ef5
Create Date: 2025-01-13 00:48:53.226603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11a1166a9bef'
down_revision: Union[str, None] = '8587cf163ef5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comments_comment_id_fkey', 'comments', type_='foreignkey')
    op.drop_constraint('comments_pin_id_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'pins', ['pin_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'comments', 'comments', ['comment_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('likes_pin_id_fkey', 'likes', type_='foreignkey')
    op.drop_constraint('likes_comment_id_fkey', 'likes', type_='foreignkey')
    op.create_foreign_key(None, 'likes', 'pins', ['pin_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'likes', 'comments', ['comment_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('pins_tags_pin_id_fkey', 'pins_tags', type_='foreignkey')
    op.create_foreign_key(None, 'pins_tags', 'pins', ['pin_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('users_pins_pin_id_fkey', 'users_pins', type_='foreignkey')
    op.create_foreign_key(None, 'users_pins', 'pins', ['pin_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_pins', type_='foreignkey')
    op.create_foreign_key('users_pins_pin_id_fkey', 'users_pins', 'pins', ['pin_id'], ['id'])
    op.drop_constraint(None, 'pins_tags', type_='foreignkey')
    op.create_foreign_key('pins_tags_pin_id_fkey', 'pins_tags', 'pins', ['pin_id'], ['id'])
    op.drop_constraint(None, 'likes', type_='foreignkey')
    op.drop_constraint(None, 'likes', type_='foreignkey')
    op.create_foreign_key('likes_comment_id_fkey', 'likes', 'comments', ['comment_id'], ['id'])
    op.create_foreign_key('likes_pin_id_fkey', 'likes', 'pins', ['pin_id'], ['id'])
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_pin_id_fkey', 'comments', 'pins', ['pin_id'], ['id'])
    op.create_foreign_key('comments_comment_id_fkey', 'comments', 'comments', ['comment_id'], ['id'])
    # ### end Alembic commands ###
