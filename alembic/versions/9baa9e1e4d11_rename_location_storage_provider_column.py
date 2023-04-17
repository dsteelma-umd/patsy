"""Rename Location.storage_provider column

Revision ID: 9baa9e1e4d11
Revises: 56cfcb965714
Create Date: 2023-04-17 14:39:35.427063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9baa9e1e4d11'
down_revision = '56cfcb965714'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("locations", "storage_provider", new_column_name="storage_provider_libitd2254")


def downgrade() -> None:
    op.alter_column("locations", "storage_provider_libitd2254", new_column_name="storage_provider")
