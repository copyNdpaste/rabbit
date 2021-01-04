"""create regions table

Revision ID: cc73bf0f602f
Revises: b844309b4fcc
Create Date: 2020-12-29 00:08:39.022347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cc73bf0f602f"
down_revision = "b844309b4fcc"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "regions",
        sa.Column(
            "id", sa.Integer().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("regions")
