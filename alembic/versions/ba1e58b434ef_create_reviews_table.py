"""create reviews table

Revision ID: ba1e58b434ef
Revises: 7376a7e14dc6
Create Date: 2025-03-07 11:20:34.284473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba1e58b434ef'
down_revision: Union[str, None] = '7376a7e14dc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
