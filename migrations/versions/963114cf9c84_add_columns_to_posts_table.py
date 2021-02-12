"""add columns to posts table

Revision ID: 963114cf9c84
Revises: 88d1fcdbbda4
Create Date: 2021-02-04 23:00:07.486043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "963114cf9c84"
down_revision = "88d1fcdbbda4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("amount", sa.SmallInteger(), nullable=True))
    op.add_column("posts", sa.Column("price_per_unit", sa.Integer(), nullable=True))
    op.add_column("posts", sa.Column("status", sa.String(length=20), nullable=False))
    op.add_column("posts", sa.Column("unit", sa.String(length=5), nullable=True))


def downgrade():
    op.drop_column("posts", "unit")
    op.drop_column("posts", "status")
    op.drop_column("posts", "price_per_unit")
    op.drop_column("posts", "amount")
