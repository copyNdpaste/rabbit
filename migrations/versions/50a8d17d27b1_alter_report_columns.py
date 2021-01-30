"""alter columns

Revision ID: 50a8d17d27b1
Revises: 29b5fc5954a8
Create Date: 2021-01-26 20:08:42.648733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "50a8d17d27b1"
down_revision = "29b5fc5954a8"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "comment_reports", "report_user_id", existing_type=sa.BIGINT(), nullable=True
    )
    op.alter_column(
        "comment_reports", "status", existing_type=sa.VARCHAR(length=20), nullable=True
    )
    op.alter_column(
        "post_reports", "report_user_id", existing_type=sa.BIGINT(), nullable=True
    )
    op.alter_column(
        "post_reports", "status", existing_type=sa.VARCHAR(length=20), nullable=True
    )


def downgrade():
    op.alter_column(
        "post_reports", "status", existing_type=sa.VARCHAR(length=20), nullable=False
    )
    op.alter_column(
        "post_reports", "report_user_id", existing_type=sa.BIGINT(), nullable=False
    )
    op.alter_column(
        "comment_reports", "status", existing_type=sa.VARCHAR(length=20), nullable=False
    )
    op.alter_column(
        "comment_reports", "report_user_id", existing_type=sa.BIGINT(), nullable=False
    )
