"""create post category table

Revision ID: 8b00c22260f6
Revises: 24163c9a3759
Create Date: 2021-02-11 13:51:13.594223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8b00c22260f6"
down_revision = "24163c9a3759"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "post_category",
        sa.Column("post_id", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column("category_id", sa.SMALLINT(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"], ["categories.id"], name="post_category_category_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["post_id"], ["posts.id"], name="post_category_post_id_fkey"
        ),
    )
    op.create_index(
        "post_id_category_id_index",
        "post_category",
        ["post_id", "category_id"],
        unique=True,
    )


def downgrade():
    op.drop_index("post_id_category_id_index", table_name="post_category")
    op.drop_table("post_category")
