"""Altering payments

Revision ID: 481ec8d76d27
Revises: 54e81c609723
Create Date: 2024-10-16 21:28:12.504725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '481ec8d76d27'
down_revision: Union[str, None] = '54e81c609723'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('receipt_path', sa.String(), nullable=True))
    op.drop_index('ix_payment_receipt_doc', table_name='payment')
    op.create_index(op.f('ix_payment_receipt_path'), 'payment', ['receipt_path'], unique=False)
    op.drop_column('payment', 'receipt_doc')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('receipt_doc', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_payment_receipt_path'), table_name='payment')
    op.create_index('ix_payment_receipt_doc', 'payment', ['receipt_doc'], unique=False)
    op.drop_column('payment', 'receipt_path')
    # ### end Alembic commands ###