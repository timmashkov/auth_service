"""add admin

Revision ID: 0001_seed
Revises: None
Create Date: 2023-11-17 15:37:01.431174

"""

import sqlalchemy as sa
from alembic import op

from infrastructure.config.config import settings
from infrastructure.database.models import Permission, Role

# revision identifiers, used by Alembic.
revision = "0003_seed"
down_revision = "0002_seed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.bulk_insert(Role.__table__, ROLES)
    op.bulk_insert(Permission.__table__, PERMISSIONS)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.delete(Role).where(Role.uuid.in_([role["uuid"] for role in ROLES])))
    op.execute(
        sa.delete(Permission).where(
            Permission.uuid.in_([perm["uuid"] for perm in PERMISSIONS])
        )
    )
    # ### end Alembic commands ###


ROLES = [
    {
        "uuid": settings.USERS.guest_role_uuid,
        "name": "guest",
    },
    {
        "uuid": settings.USERS.author_role_uuid,
        "name": "author",
    },
    {
        "uuid": settings.USERS.moderator_role_uuid,
        "name": "moderator",
    },
]

PERMISSIONS = [
    {
        "uuid": settings.USERS.create_permission_uuid,
        "name": "creator",
        "layer": "client",
    },
    {
        "uuid": settings.USERS.read_permission_uuid,
        "name": "reader",
        "layer": "client",
    },
    {
        "uuid": settings.USERS.update_permission_uuid,
        "name": "editor",
        "layer": "client",
    },
    {
        "uuid": settings.USERS.delete_permission_uuid,
        "name": "deleter",
        "layer": "client",
    },
]
