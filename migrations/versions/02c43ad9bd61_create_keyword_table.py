"""create keyword table

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
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('keywords',
                    sa.Column('user_id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
                    sa.Column('name_1', sa.String(length=50), nullable=True),
                    sa.Column('name_2', sa.String(length=50), nullable=True),
                    sa.Column('name_3', sa.String(length=50), nullable=True),
                    sa.Column('name_4', sa.String(length=50), nullable=True),
                    sa.Column('name_5', sa.String(length=50), nullable=True),
                    sa.Column('name_6', sa.String(length=50), nullable=True),
                    sa.Column('name_7', sa.String(length=50), nullable=True),
                    sa.Column('name_8', sa.String(length=50), nullable=True),
                    sa.Column('name_9', sa.String(length=50), nullable=True),
                    sa.Column('name_10', sa.String(length=50), nullable=True),
                    sa.Column('name_11', sa.String(length=50), nullable=True),
                    sa.Column('name_12', sa.String(length=50), nullable=True),
                    sa.Column('name_13', sa.String(length=50), nullable=True),
                    sa.Column('name_14', sa.String(length=50), nullable=True),
                    sa.Column('name_15', sa.String(length=50), nullable=True),
                    sa.Column('name_16', sa.String(length=50), nullable=True),
                    sa.Column('name_17', sa.String(length=50), nullable=True),
                    sa.Column('name_18', sa.String(length=50), nullable=True),
                    sa.Column('name_19', sa.String(length=50), nullable=True),
                    sa.Column('name_20', sa.String(length=50), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id']))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('keywords')
    # ### end Alembic commands ###
