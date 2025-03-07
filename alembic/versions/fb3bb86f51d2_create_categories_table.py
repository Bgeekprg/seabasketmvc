"""create categories table

Revision ID: fb3bb86f51d2
Revises: 69fd1dba6352
Create Date: 2025-03-07 11:07:47.685636

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fb3bb86f51d2"
down_revision: Union[str, None] = "69fd1dba6352"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("categoryName", sa.String(length=100), nullable=False),
        sa.Column("status", sa.Boolean(), default=True, server_default=sa.true()),
        sa.Column(
            "createdAt", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updatedAt",
            sa.DateTime(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("categories")
