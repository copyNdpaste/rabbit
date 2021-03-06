"""create notification_histories table

Revision ID: b376c4921967
Revises: 257dd4034578
Create Date: 2021-02-27 17:38:20.834397

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b376c4921967"
down_revision = "257dd4034578"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "notification_histories",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "user_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=5), nullable=True),
        sa.Column(
            "message",
            postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), "sqlite"),
            nullable=False,
        ),
        sa.Column("category", sa.String(length=5), nullable=False),
        sa.Column("type", sa.String(length=3), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("notification_histories")
