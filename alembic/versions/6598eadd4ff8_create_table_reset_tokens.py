"""create table reset_tokens

Revision ID: 6598eadd4ff8
Revises: ba1e58b434ef
Create Date: 2025-03-12 17:16:19.518856

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6598eadd4ff8"
down_revision: Union[str, None] = "ba1e58b434ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reset_tokens",
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("expires", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("token"),
        sa.ForeignKeyConstraint(["email"], ["users.email"], ondelete="CASCADE"),
    )
    op.create_index("idx_token", "reset_tokens", ["token"], unique=False)


def downgrade() -> None:
    op.drop_index("idx_token", table_name="reset_tokens")
    op.drop_table("reset_tokens")
