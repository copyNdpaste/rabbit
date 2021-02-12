"""create region group table

Revision ID: 33883a526a0e
Revises: f0d09931ed19
Create Date: 2021-01-23 14:04:07.782733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "33883a526a0e"
down_revision = "f0d09931ed19"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "region_groups",
        sa.Column(
            "id", sa.SmallInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("region_groups")
