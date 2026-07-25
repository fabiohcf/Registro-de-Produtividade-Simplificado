"""remove session goal relationship

Revision ID: 23c3095a139d
Revises: 5b937552d854
Create Date: 2026-07-25 11:18:36.345547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23c3095a139d'
down_revision: Union[str, Sequence[str], None] = '5b937552d854'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
