"""add_role_admin

Revision ID: 0001_seed
Revises: None
Create Date: 2023-11-17 15:37:01.431174

"""

import sqlalchemy as sa
from alembic import op

from application.config import settings
from infrastructure.database.models import Role

# revision identifiers, used by Alembic.
revision = "0001_seed"
down_revision = "72112e6a6208"
branch_labels = "seed"
depends_on = "72112e6a6208"


def upgrade() -> None:
    conn = op.get_bind()
    stmt = sa.select(Role.uuid).where(Role.uuid == settings.USERS.admin_role_uuid)
    result = conn.execute(stmt).first()
    if not result:
        op.execute(
            sa.insert(Role).values(name="admin", uuid=settings.USERS.admin_role_uuid)
        )


def downgrade() -> None:
    op.execute(sa.delete(Role).where(Role.uuid == settings.USERS.admin_role_uuid))
