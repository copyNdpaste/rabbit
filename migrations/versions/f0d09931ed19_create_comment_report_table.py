"""create comment report table

Revision ID: f0d09931ed19
Revises: 3e0651c8845f
Create Date: 2021-01-14 22:16:42.668557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f0d09931ed19"
down_revision = "3e0651c8845f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "comment_reports",
        sa.Column(
            "id", sa.SmallInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("comment_id", sa.BigInteger(), nullable=False),
        sa.Column("report_user_id", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, default="pending"),
        sa.Column("context", sa.String(length=100), nullable=True),
        sa.Column("confirm_admin_id", sa.Integer(), nullable=True),
        sa.Column("is_system_report", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["comment_id"], ["comments.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("comment_reports")
