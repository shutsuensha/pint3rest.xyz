"""add delete_orphaned_update trigger

Revision ID: 83e35dbc9276
Revises: 9a3359ac41b9
Create Date: 2025-04-07 00:40:05.113601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83e35dbc9276'
down_revision: Union[str, None] = '9a3359ac41b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.execute("""
    CREATE OR REPLACE FUNCTION delete_orphaned_update()
    RETURNS TRIGGER AS $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1 FROM users_recommendations_pins
        WHERE update_id = OLD.update_id AND id != OLD.id
      ) THEN
        DELETE FROM updates WHERE id = OLD.update_id;
      END IF;
      RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER trg_delete_orphaned_update
    AFTER DELETE ON users_recommendations_pins
    FOR EACH ROW
    EXECUTE FUNCTION delete_orphaned_update();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_delete_orphaned_update ON users_recommendations_pins;")
    op.execute("DROP FUNCTION IF EXISTS delete_orphaned_update;")
