"""Drop storage provider placeholder column

Revision ID: 89abe2c653c7
Revises: e397ad14ec7a
Create Date: 2023-04-17 19:21:56.419216

"""
from alembic import op
import sqlalchemy as sa
from patsy.core.schema import Schema

# revision identifiers, used by Alembic.
revision = '89abe2c653c7'
down_revision = 'e397ad14ec7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('DROP VIEW IF EXISTS patsy_records;')
    op.drop_column('locations', 'storage_provider_libitd2254')
    op.execute(Schema.get_patsy_records_view_schema())


def downgrade() -> None:
    pass
