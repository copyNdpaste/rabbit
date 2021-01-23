"""create region group foreignkey

Revision ID: 2f630c09b81c
Revises: 33883a526a0e
Create Date: 2021-01-23 14:08:54.474550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2f630c09b81c"
down_revision = "33883a526a0e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "regions", sa.Column("region_group_id", sa.SmallInteger(), nullable=False)
    )
    op.create_foreign_key(
        "regions_group_id_fkey",
        "regions",
        "region_groups",
        ["region_group_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("regions_group_id_fkey", "regions", type_="foreignkey")
    op.drop_column("regions", "region_group_id")
