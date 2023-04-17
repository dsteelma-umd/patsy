"""Add location storage provider foreign key column

Revision ID: cd384f0c7c87
Revises: 9baa9e1e4d11
Create Date: 2023-04-17 17:49:06.380365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd384f0c7c87'
down_revision = '9baa9e1e4d11'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('locations', sa.Column('storage_provider_id', sa.Integer(), nullable=True))
    op.drop_index('location_storage', table_name='locations')
#    op.create_index('location_storage', 'locations',
#                    ['storage_provider_libitd2254', 'storage_provider_libitd2254'], unique=True)
    op.create_foreign_key(None, 'locations', 'locations_type', ['storage_provider_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'locations', type_='foreignkey')
    op.drop_index('location_storage', table_name='locations')
    op.create_index('location_storage', 'locations', ['storage_provider_libitd2254', 'storage_location'], unique=False)
    op.drop_column('locations', 'storage_provider_id')
