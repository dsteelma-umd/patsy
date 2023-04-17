"""Populate Location Types table

Populate "LocationType table with unique values from the "storage_provider"
field in the "Location" table.

Revision ID: 56cfcb965714
Revises: 42adae38ad8b
Create Date: 2023-04-17 13:03:23.673894

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import column, distinct, table, text
from sqlalchemy.orm import Session
from patsy.model import LocationsType

# revision identifiers, used by Alembic.
revision = '56cfcb965714'
down_revision = '42adae38ad8b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind)

    sp_query = text(
      "SELECT DISTINCT storage_provider FROM locations"
    )
    results = session.execute(sp_query)

    sp_insert = text("INSERT INTO locations_type (storage_provider) VALUES (:sp)")
    for result in results:
        storage_provider = result[0]
        sp_insert = sp_insert.bindparams(sp=storage_provider)
        session.execute(sp_insert)


def downgrade() -> None:
    # Delete all rows in the LocationType table
    session = Session(bind=op.get_bind())
    session.query(LocationsType).delete()
    session.commit()
