"""create reviews and ratings table

Revision ID: 8213562185df
Revises: 6598eadd4ff8
Create Date: 2025-03-12 18:08:46.593968

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8213562185df"
down_revision: Union[str, None] = "6598eadd4ff8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reviews_ratings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("productId", sa.Integer(), nullable=False),
        sa.Column("userId", sa.Integer(), nullable=False),
        sa.Column("rating", sa.DECIMAL(precision=3, scale=2), nullable=True),
        sa.Column("reviewText", sa.TEXT(), nullable=True),
        sa.Column(
            "createdAt", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updatedAt",
            sa.DateTime(),
            onupdate=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["productId"],
            ["products.id"],
        ),
        sa.ForeignKeyConstraint(
            ["userId"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("reviews_ratings")
