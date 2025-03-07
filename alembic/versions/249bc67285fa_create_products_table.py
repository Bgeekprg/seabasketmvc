"""create products  table

Revision ID: 249bc67285fa
Revises: fb3bb86f51d2
Create Date: 2025-03-07 11:10:12.141107

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "249bc67285fa"
down_revision: Union[str, None] = "fb3bb86f51d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.Column("stockQuantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column(
            "categoryId", sa.Integer(), sa.ForeignKey("categories.id"), nullable=True
        ),
        sa.Column("productUrl", sa.String(length=255), nullable=True),
        sa.Column("discount", sa.Integer(), nullable=True),
        sa.Column("rating", sa.DECIMAL(precision=3, scale=2), nullable=True),
        sa.Column(
            "isAvailable", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
        sa.Column(
            "createdAt", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updatedAt",
            sa.TIMESTAMP(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("products")
