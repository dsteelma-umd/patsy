# This file stores versioned instances of the SQL SELECT statement needed to
# generate the "patsy_records" view.
#
# This is needed because both the Alembic migrations, and the PATSy tests need
# to be able to create the appropriate "patsy_records" view for the current
# state of the database.
#
# The version used for tests is set in the "create_patsy_records_view" method
# of "tests/__init__.py".
patsy_records_view_select = {
    'v2':
    '''
    SELECT
        batches.id as "batch_id",
        batches.name as "batch_name",
        accessions.id as "accession_id",
        accessions.relpath,
        accessions.filename,
        accessions.extension,
        accessions.bytes,
        accessions.timestamp,
        accessions.md5,
        accessions.sha1,
        accessions.sha256,
        locations.id as "location_id",
        storage_providers.storage_provider,
        locations.storage_location
        FROM batches
        LEFT JOIN accessions ON batches.id = accessions.batch_id
        LEFT JOIN accession_locations ON accessions.id = accession_locations.accession_id
        LEFT JOIN locations ON accession_locations.location_id = locations.id
        LEFT JOIN storage_providers ON locations.storage_provider_id = storage_providers.id
        ORDER BY batches.id
    ''',
    # Version 1
    'v1':
    '''
    SELECT
        batches.id as "batch_id",
        batches.name as "batch_name",
        accessions.id as "accession_id",
        accessions.relpath,
        accessions.filename,
        accessions.extension,
        accessions.bytes,
        accessions.timestamp,
        accessions.md5,
        accessions.sha1,
        accessions.sha256,
        locations.id as "location_id",
        locations.storage_provider,
        locations.storage_location
        FROM batches
        LEFT JOIN accessions ON batches.id = accessions.batch_id
        LEFT JOIN accession_locations ON accessions.id = accession_locations.accession_id
        LEFT JOIN locations ON accession_locations.location_id = locations.id
        ORDER BY batches.id
    '''
}
