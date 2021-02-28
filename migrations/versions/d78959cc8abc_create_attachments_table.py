"""create attachments table

Revision ID: d78959cc8abc
Revises: 257dd4034578
Create Date: 2021-02-22 21:43:26.665355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d78959cc8abc"
down_revision = "257dd4034578"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "attachments",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("type", sa.String(length=10), nullable=False),
        sa.Column("uuid", sa.String(length=50), nullable=False),
        sa.Column("file_name", sa.String(length=50), nullable=False),
        sa.Column("path", sa.String(length=50), nullable=False),
        sa.Column("extension", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("attachments")
