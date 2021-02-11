"""create categories table

Revision ID: 24163c9a3759
Revises: 3e816b271743
Create Date: 2021-02-11 13:49:30.223733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "24163c9a3759"
down_revision = "3e816b271743"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("categories")
