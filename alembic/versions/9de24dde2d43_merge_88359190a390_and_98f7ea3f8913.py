"""Merge 88359190a390 and 98f7ea3f8913

Revision ID: 9de24dde2d43
Revises: 98f7ea3f8913
Create Date: 2024-10-14 19:31:03.872908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9de24dde2d43'
down_revision = ('88359190a390', '98f7ea3f8913')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
