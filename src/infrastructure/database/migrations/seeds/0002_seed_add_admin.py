"""add admin

Revision ID: 0001_seed
Revises: None
Create Date: 2023-11-17 15:37:01.431174

"""

import sqlalchemy as sa
from alembic import op

from application.config import settings
from application.container import Container
from infrastructure.database.models import Role, User

# revision identifiers, used by Alembic.
revision = "0002_seed"
down_revision = "0001_seed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    auth_handler = Container.auth_handler()
    salted_pass = auth_handler.encode_pass(
        settings.USERS.default_superuser.password,
        settings.USERS.default_superuser.login,
    )
    conn = op.get_bind()
    with sa.orm.Session(bind=conn) as session:
        try:
            stmt = (
                sa.select(User)
                .where(
                    User.is_active.is_(True),
                    User.is_verified.is_(True),
                    User.roles.any(Role.name.in_(settings.USERS.superuser_roles)),
                )
                .limit(1)
            )
            user = session.execute(stmt).scalar_one_or_none()
            if not user:
                role_stmt = sa.select(Role).where(
                    Role.uuid == settings.USERS.admin_role_uuid
                )
                role = session.execute(role_stmt).scalar()
                user = User(
                    login=settings.USERS.default_superuser.login,
                    hashed_password=salted_pass,
                    is_superuser=True,
                    is_active=True,
                    is_verified=True,
                    age=33,
                    email=settings.USERS.default_superuser.email,
                    phone_number=str(settings.USERS.default_superuser.phone_number),
                    roles=[role],
                )
                session.add(user)
                session.commit()
            else:
                print(f"Superuser already exists {user.login}")
        except Exception as e:  # noqa
            session.rollback()
            print(f"Skip create superuser: {e}")


def downgrade() -> None:
    conn = op.get_bind()
    with sa.orm.Session(bind=conn) as session:
        user_stmt = sa.select(User).where(
            User.login == settings.USERS.default_superuser.login
        )
        user = session.execute(user_stmt).scalar()
        if user:
            session.delete(user)
            session.commit()
