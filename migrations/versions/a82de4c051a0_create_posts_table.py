"""create posts table

Revision ID: a82de4c051a0
Revises: cdf3a4bae909
Create Date: 2020-12-29 00:43:49.707887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a82de4c051a0"
down_revision = "cdf3a4bae909"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "user_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("region_group_id", sa.SmallInteger, nullable=False),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("is_comment_disabled", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("is_blocked", sa.Boolean(), nullable=False),
        sa.Column("report_count", sa.Integer(), nullable=True),
        sa.Column("read_count", sa.Integer(), nullable=True),
        sa.Column("category", sa.Integer(), nullable=False),
        sa.Column("last_user_action", sa.String(length=20), nullable=False),
        sa.Column("last_user_action_at", sa.DateTime(), nullable=True),
        sa.Column("last_admin_action", sa.String(length=20), nullable=False),
        sa.Column("last_admin_action_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("posts")
