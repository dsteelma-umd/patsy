"""LIBITD-2254. Change locations storage provider field to relationship

Revision ID: 9f2e1ad09f96
Revises: 8d5c49f4b160
Create Date: 2023-04-20 15:03:47.547450

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.orm import Session
from patsy.model import StorageProvider

# revision identifiers, used by Alembic.
revision = '9f2e1ad09f96'
down_revision = '8d5c49f4b160'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index('location_storage', table_name='locations')
    op.create_index('location_storage', 'locations', ['storage_provider_id', 'storage_location'], unique=True)
    op.drop_column('locations', 'storage_provider')


def downgrade() -> None:
    op.add_column('locations', sa.Column('storage_provider', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index('location_storage', table_name='locations')

    bind = op.get_bind()
    session = Session(bind)

    # Repopulate "storage_provider" with information from "storage_provider_id"
    storage_providers = session.query(StorageProvider)
    for storage_provider in storage_providers:
        sp_id = storage_provider.id
        sp_name = storage_provider.storage_provider

        update_query = text(
            """
            UPDATE locations
            SET storage_provider = :storage_provider
            WHERE storage_provider_id = :storage_provider_id
            """
        )
        update_query = update_query.bindparams(
            storage_provider_id=f"{sp_id}",
            storage_provider=f"{sp_name}"
        )
        session.execute(update_query)

    op.create_index('location_storage', 'locations', ['storage_provider', 'storage_location'], unique=False)
