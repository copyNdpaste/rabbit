"""merge_split_heads

Revision ID: 6b86a939effb
Revises: 851cac98af63, d78959cc8abc
Create Date: 2021-03-11 23:27:28.726590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6b86a939effb"
down_revision = ("851cac98af63", "d78959cc8abc")
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
