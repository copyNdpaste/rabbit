"""create post report table

Revision ID: 3e0651c8845f
Revises: 966108d0abb7
Create Date: 2021-01-14 22:14:25.745096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3e0651c8845f"
down_revision = "966108d0abb7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "post_reports",
        sa.Column(
            "id", sa.SmallInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("report_user_id", sa.BigInteger(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("context", sa.String(length=100), nullable=True),
        sa.Column("confirm_admin_id", sa.Integer(), nullable=True),
        sa.Column("is_system_report", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("post_reports")
