"""modify comment columns

Revision ID: 04b54888f494
Revises: 50a8d17d27b1
Create Date: 2021-01-30 21:10:39.478604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "04b54888f494"
down_revision = "50a8d17d27b1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("comments", sa.Column("body", sa.String(length=500), nullable=True))
    op.add_column("comments", sa.Column("is_blocked", sa.Boolean(), nullable=False))
    op.add_column("comments", sa.Column("is_deleted", sa.Boolean(), nullable=False))
    op.add_column(
        "comments", sa.Column("last_admin_action", sa.String(length=20), nullable=False)
    )
    op.add_column(
        "comments", sa.Column("last_admin_action_at", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "comments", sa.Column("last_user_action", sa.String(length=20), nullable=False)
    )
    op.add_column(
        "comments", sa.Column("last_user_action_at", sa.DateTime(), nullable=True)
    )
    op.add_column("comments", sa.Column("report_count", sa.Integer(), nullable=True))
    op.drop_column("comments", "is_system_report")
    op.drop_column("comments", "context")
    op.drop_column("comments", "status")
    op.drop_column("comments", "confirm_admin_id")
    op.drop_column("comments", "report_user_id")


def downgrade():
    op.add_column(
        "comments",
        sa.Column("report_user_id", sa.BIGINT(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "comments",
        sa.Column("confirm_admin_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "comments",
        sa.Column("status", sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    )
    op.add_column(
        "comments",
        sa.Column("context", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    )
    op.add_column(
        "comments",
        sa.Column("is_system_report", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.drop_column("comments", "report_count")
    op.drop_column("comments", "last_user_action_at")
    op.drop_column("comments", "last_user_action")
    op.drop_column("comments", "last_admin_action_at")
    op.drop_column("comments", "last_admin_action")
    op.drop_column("comments", "is_deleted")
    op.drop_column("comments", "is_blocked")
    op.drop_column("comments", "body")
