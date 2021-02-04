"""create post like counts table

Revision ID: 88d1fcdbbda4
Revises: 1fdc8203583a
Create Date: 2021-02-04 22:43:41.533654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "88d1fcdbbda4"
down_revision = "1fdc8203583a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "post_like_counts",
        sa.Column(
            "id", sa.SmallInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("post_like_counts")
