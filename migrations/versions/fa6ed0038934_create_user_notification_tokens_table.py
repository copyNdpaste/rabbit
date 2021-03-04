"""create user_notification_tokens table

Revision ID: fa6ed0038934
Revises: 02c43ad9bd61
Create Date: 2021-03-03 10:38:32.478646

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "fa6ed0038934"
down_revision = "02c43ad9bd61"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_notification_tokens",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "user_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("token", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("user_notification_tokens")
