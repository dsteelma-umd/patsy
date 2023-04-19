"""LIBITD-2254. Add storage_provider values

Retrieves the unique list of storage provider names from the
"locations" table, and adds them to the "storage_providers" table.

Revision ID: 05e4fcd6b3a5
Revises: 7f2b8452d4a0
Create Date: 2023-04-19 16:03:23.090032

"""
from alembic import op
from sqlalchemy import text
from sqlalchemy.orm import Session
from patsy.model import StorageProvider

# revision identifiers, used by Alembic.
revision = '05e4fcd6b3a5'
down_revision = '7f2b8452d4a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind)

    sp_query = text(
      "SELECT DISTINCT storage_provider FROM locations"
    )
    results = session.execute(sp_query)

    sp_insert = text("INSERT INTO storage_providers (storage_provider) VALUES (:sp)")
    for result in results:
        storage_provider = result[0]
        sp_insert = sp_insert.bindparams(sp=storage_provider)
        session.execute(sp_insert)


def downgrade() -> None:
    # Delete all rows in the StorageProvider table
    session = Session(bind=op.get_bind())
    session.query(StorageProvider).delete()
    session.commit()
