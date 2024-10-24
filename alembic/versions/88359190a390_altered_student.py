"""altered student

Revision ID: 88359190a390
Revises: 00f30cc14aaf
Create Date: 2024-09-28 01:01:17.566847

"""
from typing import Sequence, Union
from sqlalchemy.engine.reflection import Inspector

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88359190a390'
down_revision: Union[str, None] = '00f30cc14aaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Get the current connection and inspect the table structure
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    # Check if the 'image_path' column exists
    columns = [col['name'] for col in inspector.get_columns('student')]
    
    if 'image_path' not in columns:
        op.add_column('student', sa.Column('image_path', sa.String(), nullable=True))

def downgrade():
    # Drop the 'image_path' column only if it exists
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('student')]

    if 'image_path' in columns:
        op.drop_column('student', 'image_path')
