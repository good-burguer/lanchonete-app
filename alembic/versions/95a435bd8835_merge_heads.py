"""merge heads

Revision ID: 95a435bd8835
Revises: 7a2d7ea02841, 8b5c4d1a2f3e
Create Date: 2025-09-29 17:57:09.389109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95a435bd8835'
down_revision: Union[str, None] = ('7a2d7ea02841', '8b5c4d1a2f3e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
