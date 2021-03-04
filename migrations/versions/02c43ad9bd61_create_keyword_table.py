"""create keywords table

Revision ID: 02c43ad9bd61
Revises: b376c4921967
Create Date: 2021-02-27 19:24:57.927790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02c43ad9bd61'
down_revision = 'b376c4921967'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('keywords',
                    sa.Column('user_id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
                    sa.Column('name_1', sa.String(length=50), nullable=True),
                    sa.Column('name_2', sa.String(length=50), nullable=True),
                    sa.Column('name_3', sa.String(length=50), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id']))


def downgrade():
    op.drop_table('keywords')
