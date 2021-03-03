"""create notifications table

Revision ID: 851cac98af63
Revises: fa6ed0038934
Create Date: 2021-03-03 11:31:07.024537

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '851cac98af63'
down_revision = 'fa6ed0038934'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "notifications",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "user_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column("use_bantime", sa.Boolean(), nullable=False),
        sa.Column("use_keyword", sa.Boolean(), nullable=False),
        sa.Column("use_chat", sa.Integer(), nullable=False),
        sa.Column("use_etc", sa.Boolean(), nullable=False),
        sa.Column("ban_time_from", sa.String(length=4), nullable=False),
        sa.Column("ban_time_to", sa.String(length=4), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("notifications")
