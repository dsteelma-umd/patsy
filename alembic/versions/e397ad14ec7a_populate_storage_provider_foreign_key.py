"""Populate storage provider foreign key

Revision ID: e397ad14ec7a
Revises: cd384f0c7c87
Create Date: 2023-04-17 17:59:02.110964

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.orm import Session
from patsy.model import LocationsType, Location

# revision identifiers, used by Alembic.
revision = 'e397ad14ec7a'
down_revision = 'cd384f0c7c87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind)

    locations_types = session.query(LocationsType)
    for loc_type in locations_types:
        loc_id = loc_type.id
        loc_storage_provider = loc_type.storage_provider

        update_query = text(
            """
            UPDATE locations
            SET storage_provider_id = :storage_provider_id
            WHERE storage_provider_id is NULL
            AND storage_provider_libitd2254 = :storage_provider
            """
        )
        update_query = update_query.bindparams(
            storage_provider_id=f"{loc_id}", storage_provider=f"{loc_storage_provider}"
        )
        session.execute(update_query)


def downgrade() -> None:
    pass
