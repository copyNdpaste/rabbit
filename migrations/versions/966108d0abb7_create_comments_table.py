"""create comments table

Revision ID: 966108d0abb7
Revises: cabdbb764bbf
Create Date: 2021-01-13 01:10:05.868964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "966108d0abb7"
down_revision = "cabdbb764bbf"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "comments",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("parent_id", sa.BigInteger(), nullable=False),
        sa.Column("report_user_id", sa.BigInteger(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("context", sa.String(length=50), nullable=True),
        sa.Column("confirm_admin_id", sa.Integer(), nullable=True),
        sa.Column("is_system_report", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["comments.id"],),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"],),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("comments")
