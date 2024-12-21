"""alt value and fee to string because of >int64 values

Revision ID: a664a1da91a9
Revises: 408e1c145975
Create Date: 2024-12-21 11:32:33.786477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a664a1da91a9'
down_revision = '408e1c145975'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'value',
               existing_type=sa.BIGINT(),
               type_=sa.String(),
               existing_nullable=False)
    op.alter_column('transactions', 'fee',
               existing_type=sa.BIGINT(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'fee',
               existing_type=sa.String(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('transactions', 'value',
               existing_type=sa.String(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    # ### end Alembic commands ###
