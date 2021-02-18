"""drop category column of post table

Revision ID: 3e816b271743
Revises: 8960859423f9
Create Date: 2021-02-11 13:48:18.043074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3e816b271743"
down_revision = "8960859423f9"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("posts", "category")


def downgrade():
    op.add_column(
        "posts",
        sa.Column("category", sa.INTEGER(), autoincrement=False, nullable=False),
    )
