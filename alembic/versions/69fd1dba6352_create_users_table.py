"""create users table

Revision ID: 69fd1dba6352
Revises:
Create Date: 2025-03-07 11:05:13.629494

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "69fd1dba6352"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False, unique=True),
        sa.Column("phoneNumber", sa.String(length=13), nullable=True, unique=True),
        sa.Column("password", sa.String(length=80), nullable=False),
        sa.Column("profilePic", sa.String(length=255), nullable=True),
        sa.Column(
            "role",
            sa.Enum("admin", "customer", name="role"),
            nullable=False,
            server_default="customer",
        ),
        sa.Column("status", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "isVerified", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column(
            "createdAt", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updatedAt",
            sa.DateTime(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_name"), "users", ["name"], unique=False)
    op.create_index(op.f("ix_users_phoneNumber"), "users", ["phoneNumber"], unique=True)


def downgrade() -> None:
    op.drop_table("users")
