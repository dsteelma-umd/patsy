"""LIBITD-2254. Link locations to storage providers table

Note: Downgrading this migration will result in DATA LOSS if the
"storage_provider_id" column contained data prior to the upgrade.

Revision ID: 8d5c49f4b160
Revises: 05e4fcd6b3a5
Create Date: 2023-04-19 16:29:47.426877

"""
from alembic import op
from sqlalchemy import text
from sqlalchemy.orm import Session
from patsy.alembic.patsy_record_views_sql import patsy_records_view_select
from patsy.alembic.helpers.replaceable_objects import ReplaceableObject
from patsy.model import StorageProvider

# revision identifiers, used by Alembic.
revision = '8d5c49f4b160'
down_revision = '05e4fcd6b3a5'
branch_labels = None
depends_on = None

patsy_records_view = ReplaceableObject(
    "patsy_records",
    patsy_records_view_select['v2']
)


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind)

    storage_providers = session.query(StorageProvider)
    for storage_provider in storage_providers:
        sp_id = storage_provider.id
        sp_name = storage_provider.storage_provider

        update_query = text(
            """
            UPDATE locations
            SET storage_provider_id = :storage_provider_id
            WHERE storage_provider_id is NULL
            AND storage_provider = :storage_provider
            """
        )
        update_query = update_query.bindparams(
            storage_provider_id=f"{sp_id}",
            storage_provider=f"{sp_name}"
        )
        session.execute(update_query)

    op.execute("DROP VIEW IF EXISTS patsy_records;")
    op.create_view(patsy_records_view)


def downgrade() -> None:
    # Clear "storage_provider_id" column in all rows of the "locations" table.
    # Note: This will result in DATA LOSS if the "storage_provider_id" column
    # contained data prior to the upgrade.
    session = Session(bind=op.get_bind())
    update_query = text(
      """
     UPDATE locations SET storage_provider_id = NULL;
     """
    )
    session.execute(update_query)
