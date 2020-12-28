"""create user profiles table

Revision ID: b844309b4fcc
Revises: 
Create Date: 2020-12-28 23:24:27.401396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b844309b4fcc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_profiles",
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("uuid", sa.String(length=50), nullable=False),
        sa.Column("file_name", sa.String(length=50), nullable=False),
        sa.Column("path", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("user_profiles")
