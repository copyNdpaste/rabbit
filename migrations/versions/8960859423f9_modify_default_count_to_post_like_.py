"""modify default count to post like counts table

Revision ID: 8960859423f9
Revises: 963114cf9c84
Create Date: 2021-02-06 16:57:52.381745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8960859423f9"
down_revision = "963114cf9c84"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name="post_like_counts",
        column_name="count",
        nullable=False,
        server_default="0",
    )


def downgrade():
    op.alter_column(
        table_name="post_like_counts",
        column_name="count",
        nullable=True,
        server_default=None,
    )
