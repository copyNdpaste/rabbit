"""create post like states table

Revision ID: 1fdc8203583a
Revises: 04b54888f494
Create Date: 2021-02-04 22:19:25.556152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1fdc8203583a"
down_revision = "04b54888f494"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "post_like_states",
        sa.Column(
            "id", sa.SmallInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("state", sa.String(length=10), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"],),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "post_id_user_id_index", "post_like_states", ["post_id", "user_id"], unique=True
    )


def downgrade():
    op.drop_index("post_id_user_id_index", table_name="post_like_states")
    op.drop_table("post_like_states")
