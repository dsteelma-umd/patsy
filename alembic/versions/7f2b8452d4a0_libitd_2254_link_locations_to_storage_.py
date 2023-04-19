"""LIBITD-2254. Link locations to storage_providers

Revision ID: 7f2b8452d4a0
Revises: 2e9547b223ac
Create Date: 2023-04-19 15:58:05.511469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f2b8452d4a0'
down_revision = '2e9547b223ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('locations', sa.Column('storage_provider_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f('fk_locations_storage_provider_id_storage_providers'),
        'locations', 'storage_providers', ['storage_provider_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(op.f('fk_locations_storage_provider_id_storage_providers'), 'locations', type_='foreignkey')
    op.drop_column('locations', 'storage_provider_id')
