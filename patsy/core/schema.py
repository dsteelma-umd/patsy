from patsy.core.db_gateway import DbGateway
from patsy.model import Base


class Schema:
    def __init__(self, gateway: DbGateway) -> None:
        self.gateway = gateway

    def create_schema(self) -> None:
        session = self.gateway.session
        engine = session.get_bind()
        # print("Creating the schema using the declarative base...")
        Base.metadata.create_all(engine)

        # Create "patsy_records" view
        with engine.connect() as con:
            con.execute("DROP VIEW IF EXISTS patsy_records;")
            con.execute(Schema.get_patsy_records_view_schema())

    def get_patsy_records_view_schema():
        return """
                CREATE VIEW patsy_records AS
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
                        locations_type.storage_provider
                        FROM batches
                        LEFT JOIN accessions ON batches.id = accessions.batch_id
                        LEFT JOIN accession_locations ON accessions.id = accession_locations.accession_id
                        LEFT JOIN locations ON accession_locations.location_id = locations.id
                        LEFT JOIN locations_type ON locations_type.id = locations.storage_provider_id
                        ORDER BY batches.id
               """
