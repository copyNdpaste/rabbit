"""add region group foreignkey to post table

Revision ID: 29b5fc5954a8
Revises: 2f630c09b81c
Create Date: 2021-01-26 20:04:36.578472

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "29b5fc5954a8"
down_revision = "2f630c09b81c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        "post_regions_group_id_fkey",
        "posts",
        "region_groups",
        ["region_group_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint("post_regions_group_id_fkey", "posts", type_="foreignkey")
