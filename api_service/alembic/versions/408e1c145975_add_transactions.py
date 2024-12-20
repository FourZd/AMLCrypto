"""add transactions

Revision ID: 408e1c145975
Revises: 
Create Date: 2024-12-20 22:02:09.470996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '408e1c145975'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('block_id', sa.BigInteger(), nullable=False),
    sa.Column('index', sa.String(), nullable=True),
    sa.Column('hash', sa.String(), nullable=True),
    sa.Column('time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sender', sa.String(), nullable=True),
    sa.Column('recipient', sa.String(), nullable=False),
    sa.Column('value', sa.BigInteger(), nullable=False),
    sa.Column('fee', sa.BigInteger(), nullable=True),
    sa.Column('gas_limit', sa.BigInteger(), nullable=False),
    sa.Column('gas_price', sa.BigInteger(), nullable=True),
    sa.Column('input_hex', sa.String(), nullable=True),
    sa.Column('nonce', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_block_id'), 'transactions', ['block_id'], unique=False)
    op.create_index(op.f('ix_transactions_hash'), 'transactions', ['hash'], unique=False)
    op.create_index(op.f('ix_transactions_recipient'), 'transactions', ['recipient'], unique=False)
    op.create_index(op.f('ix_transactions_sender'), 'transactions', ['sender'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_sender'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_recipient'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_hash'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_block_id'), table_name='transactions')
    op.drop_table('transactions')
    # ### end Alembic commands ###
