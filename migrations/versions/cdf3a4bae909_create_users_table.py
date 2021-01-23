"""create users table

Revision ID: cdf3a4bae909
Revises: cc73bf0f602f
Create Date: 2020-12-29 00:32:05.902030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cdf3a4bae909"
down_revision = "cc73bf0f602f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("login_id", sa.String(length=50), nullable=False),
        sa.Column("nickname", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=50), nullable=False),
        sa.Column(
            "profile_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=10), nullable=False),
        sa.Column("provider", sa.String(length=20), nullable=False),
        sa.Column("region_id", sa.SmallInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["profile_id"], ["user_profiles.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["region_id"], ["regions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("users")
