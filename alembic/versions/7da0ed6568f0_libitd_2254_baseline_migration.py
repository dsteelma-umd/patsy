"""LIBITD-2254. Baseline migration

Creates the database based on currently existing models.

This migration replaces the PATSy "schema" command.

This migration checks whether the database tables already exist before
creating them. This enables the migration to be run against a database
with existing data, without loss.

This migration also renames primary keys and foreign keys (by dropping and
recreating them) to use the MetaData naming conventions specified in the
"patsy/model.py" file.

Note: Downgrading this migration will result in tables being dropped, and
      data (if any) will be lost.

Revision ID: 7da0ed6568f0
Revises:
Create Date: 2023-04-19 11:58:42.683509

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
from patsy.model import patsy_records_view_sql

# revision identifiers, used by Alembic.
revision = '7da0ed6568f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    if not table_exists('batches'):
        op.create_table('batches',
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('name', sa.String(), nullable=True),
                        sa.PrimaryKeyConstraint('id', name=op.f('pk_batches'))
                        )
        op.create_index('batch_name', 'batches', ['name'], unique=False)

    if not table_exists('locations'):
        op.create_table('locations',
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('storage_provider', sa.String(), nullable=True),
                        sa.Column('storage_location', sa.String(), nullable=True),
                        sa.PrimaryKeyConstraint('id', name=op.f('pk_locations'))
                        )
        op.create_index('location_storage', 'locations', ['storage_provider', 'storage_location'], unique=True)

    if not table_exists('accessions'):
        op.create_table('accessions',
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('batch_id', sa.Integer(), nullable=True),
                        sa.Column('relpath', sa.String(), nullable=True),
                        sa.Column('filename', sa.String(), nullable=True),
                        sa.Column('extension', sa.String(), nullable=True),
                        sa.Column('bytes', sa.BigInteger(), nullable=True),
                        sa.Column('timestamp', sa.String(), nullable=True),
                        sa.Column('md5', sa.String(), nullable=True),
                        sa.Column('sha1', sa.String(), nullable=True),
                        sa.Column('sha256', sa.String(), nullable=True),
                        sa.ForeignKeyConstraint(
                            ['batch_id'], ['batches.id'], name=op.f('fk_accessions_batch_id_batches')
                        ),
                        sa.PrimaryKeyConstraint('id', name=op.f('pk_accessions'))
                        )
        op.create_index('accession_batch_relpath', 'accessions', ['batch_id', 'relpath'], unique=True)

    if not table_exists('accession_locations'):
        op.create_table('accession_locations',
                        sa.Column('accession_id', sa.Integer(), nullable=True),
                        sa.Column('location_id', sa.Integer(), nullable=True),
                        sa.ForeignKeyConstraint(
                            ['accession_id'], ['accessions.id'],
                            name=op.f('fk_accession_locations_accession_id_accessions'), ondelete='CASCADE'
                        ),
                        sa.ForeignKeyConstraint(
                            ['location_id'], ['locations.id'],
                            name=op.f('fk_accession_locations_location_id_locations')
                        )
                        )
        op.create_index('accession_locations_accession_id', 'accession_locations', ['accession_id'], unique=False)
        op.create_index('accession_locations_location_id', 'accession_locations', ['location_id'], unique=False)

    # Modify primary and foreign keys to have names using MetaData naming
    # convention, if necessary.

    # Drop all the foreign keys being renamed first, as they have dependencies
    # on the primary keys
    if foreign_key_exists('accessions', u'accessions_batch_id_fkey'):
        op.drop_constraint(u'accessions_batch_id_fkey', 'accessions', type_='foreignkey')

    if foreign_key_exists('accession_locations', u'accession_locations_accession_id_fkey'):
        op.drop_constraint(u'accession_locations_accession_id_fkey', 'accession_locations', type_='foreignkey')

    if foreign_key_exists('accession_locations', u'accession_locations_location_id_fkey'):
        op.drop_constraint(u'accession_locations_location_id_fkey', 'accession_locations', type_='foreignkey')

    # Drop and recreate the primary keys
    if primary_key_exists('batches', u'batches_pkey'):
        op.drop_constraint(u'batches_pkey', 'batches', type_='primary')
        op.create_primary_key(op.f('pk_batches'), 'batches', ['id'])

    if primary_key_exists('locations', u'locations_pkey'):
        op.drop_constraint(u'locations_pkey', 'locations', type_='primary')
        op.create_primary_key(op.f('pk_locations'), 'locations', ['id'])

    if primary_key_exists('accessions', u'accessions_pkey'):
        op.drop_constraint(u'accessions_pkey', 'accessions', type_='primary')
        op.create_primary_key(op.f('pk_accessions'), 'accessions', ['id'])

    # Recreate the foreign keys with names consistent with auto-generated names
    if not foreign_key_exists('accession_locations', u'fk_accession_locations_location_id_locations'):
        op.create_foreign_key(
            op.f('fk_accession_locations_location_id_locations'),
            'accession_locations', 'locations', ['location_id'], ['id']
        )

    if not foreign_key_exists('accession_locations', u'fk_accession_locations_accession_id_accessions'):
        op.create_foreign_key(
            op.f('fk_accession_locations_accession_id_accessions'),
            'accession_locations', 'accessions', ['accession_id'], ['id'], ondelete='CASCADE'
        )

    if not foreign_key_exists('accessions', u'fk_accessions_batch_id_batches'):
        op.create_foreign_key(op.f('fk_accessions_batch_id_batches'), 'accessions', 'batches', ['batch_id'], ['id'])

    # Create the "patsy_records" View
    create_patsy_records_view()


def downgrade() -> None:
    drop_patsy_records_view()
    op.drop_index('accession_locations_location_id', table_name='accession_locations')
    op.drop_index('accession_locations_accession_id', table_name='accession_locations')
    op.drop_table('accession_locations')
    op.drop_index('accession_batch_relpath', table_name='accessions')
    op.drop_table('accessions')
    op.drop_index('location_storage', table_name='locations')
    op.drop_table('locations')
    op.drop_index('batch_name', table_name='batches')
    op.drop_table('batches')


def table_exists(table_name):
    """Returns True if a table with the given name exists, False otherwise."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    return table_name in tables


def primary_key_exists(table_name, primary_key_name):
    """
    Returns True if a primary key with the given name exists for the table,
    False otherwise.
    """
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    pk = inspector.get_pk_constraint(table_name)
    return pk['name'] == primary_key_name


def foreign_key_exists(table_name, foreign_key_name):
    """
    Returns True if a foreign key with the given name exists for the table,
    False otherwise.
    """
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    foreign_keys = inspector.get_foreign_keys(table_name)
    for fk in foreign_keys:
        if fk['name'] == foreign_key_name:
            return True

    return False


def create_patsy_records_view() -> None:
    """Drops and recreates the "patsy_records" View"""
    drop_patsy_records_view()
    op.execute(patsy_records_view_sql())


def drop_patsy_records_view() -> None:
    """Drops the "patsy_records" View"""
    op.execute("DROP VIEW IF EXISTS patsy_records;")
