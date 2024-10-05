"""add admin

Revision ID: 0001_seed
Revises: None
Create Date: 2023-11-17 15:37:01.431174

"""

import sqlalchemy as sa
from alembic import op

from application.config import settings
from infrastructure.database.models import RolePermission

# revision identifiers, used by Alembic.
revision = "0004_seed"
down_revision = "0003_seed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.bulk_insert(RolePermission.__table__, ROLE_PERMISSIONS)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        sa.delete(RolePermission).where(
            sa.or_(
                *[
                    sa.and_(
                        RolePermission.role_uuid == role_permission_seed["role_uuid"],
                        RolePermission.permission_uuid
                        == role_permission_seed["permission_uuid"],
                    )
                    for role_permission_seed in ROLE_PERMISSIONS
                ]
            )
        )
    )
    # ### end Alembic commands ###


ROLE_PERMISSIONS = [
    {
        "role_uuid": settings.USERS.admin_role_uuid,
        "permission_uuid": settings.USERS.create_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.admin_role_uuid,
        "permission_uuid": settings.USERS.read_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.admin_role_uuid,
        "permission_uuid": settings.USERS.update_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.admin_role_uuid,
        "permission_uuid": settings.USERS.delete_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.moderator_role_uuid,
        "permission_uuid": settings.USERS.create_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.moderator_role_uuid,
        "permission_uuid": settings.USERS.read_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.moderator_role_uuid,
        "permission_uuid": settings.USERS.update_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.moderator_role_uuid,
        "permission_uuid": settings.USERS.delete_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.author_role_uuid,
        "permission_uuid": settings.USERS.create_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.author_role_uuid,
        "permission_uuid": settings.USERS.read_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.author_role_uuid,
        "permission_uuid": settings.USERS.update_permission_uuid,
    },
    {
        "role_uuid": settings.USERS.guest_role_uuid,
        "permission_uuid": settings.USERS.read_permission_uuid,
    },
]
