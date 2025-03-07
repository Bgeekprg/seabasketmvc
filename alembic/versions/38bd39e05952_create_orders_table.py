"""create orders table

Revision ID: 38bd39e05952
Revises: def283fe37d8
Create Date: 2025-03-07 11:16:24.658584

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "38bd39e05952"
down_revision: Union[str, None] = "def283fe37d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("userId", sa.Integer(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=True),
        sa.Column("totalAmount", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column(
            "orderStatus",
            sa.Enum(
                "pending", "shipped", "delivered", "cancelled", name="order_status"
            ),
            default="pending",
            server_default="pending",
            nullable=True,
        ),
        sa.Column(
            "paymentStatus",
            sa.Enum("pending", "paid", "failed", "refunded", name="payment_status"),
            default="pending",
            server_default="pending",
            nullable=True,
        ),
        sa.Column("shippingAddress", sa.TEXT(), nullable=False),
        sa.Column(
            "createdAt", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updatedAt",
            sa.DateTime(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["userId"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("orders")
