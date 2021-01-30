"""create articles table

Revision ID: cabdbb764bbf
Revises: a82de4c051a0
Create Date: 2021-01-13 00:37:41.122524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cabdbb764bbf"
down_revision = "a82de4c051a0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "articles",
        sa.Column(
            "id", sa.SmallInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "post_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("body", sa.String(length=2000), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("articles")
