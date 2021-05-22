"""create index to region_group_id of posts

Revision ID: 257dd4034578
Revises: 8b00c22260f6
Create Date: 2021-02-11 19:34:36.012119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "257dd4034578"
down_revision = "8b00c22260f6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("region_group_id_index", "posts", ["region_group_id"], unique=False)


def downgrade():
    op.drop_index("region_group_id_index", table_name="posts")
