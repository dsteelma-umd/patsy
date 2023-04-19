from sqlalchemy import Column, Integer, String, Index, ForeignKey, Table, BigInteger, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Set naming conventions for constraints.
# See https://alembic.sqlalchemy.org/en/latest/naming.html
#
# This ensures that constraints are named consistently, to enable them
# to be easily handled in Alembic database migrations
Base.metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

# Many-to-many relationship between accessions and locations
accession_locations_table = Table('accession_locations', Base.metadata,
                                  Column('accession_id', Integer, ForeignKey('accessions.id', ondelete='CASCADE')),
                                  Column('location_id', Integer, ForeignKey('locations.id')))

Index('accession_locations_accession_id', accession_locations_table.c.accession_id, unique=False)
Index('accession_locations_location_id', accession_locations_table.c.location_id, unique=False)


class Batch(Base):  # type: ignore
    """
    Class representing a batch
    """

    __tablename__ = "batches"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self) -> str:
        return f"<Batch(id='{self.id}', name='{self.name}'>"


class Accession(Base):  # type: ignore
    """
    Class representing an authoritative accession record listing
    """

    __tablename__ = "accessions"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey('batches.id'))
    relpath = Column(String)
    filename = Column(String)
    extension = Column(String)
    bytes = Column(BigInteger)
    timestamp = Column(String)
    md5 = Column(String)
    sha1 = Column(String)
    sha256 = Column(String)

    batch = relationship("Batch", back_populates="accessions")
    locations = relationship(
        "Location", secondary=accession_locations_table, back_populates="accessions")

    def __repr__(self) -> str:
        return f"<Accession(id='{self.id}', batch='{self.batch}', relpath='{self.relpath}'>"


Batch.accessions = relationship("Accession", order_by=Accession.id, back_populates="batch")

Index('batch_name', Batch.name)
Index('accession_batch_relpath', Accession.batch_id, Accession.relpath, unique=True)


class Location(Base):  # type: ignore
    """
    Class representing a storage location for an accession.
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    storage_provider = Column(String)
    storage_location = Column(String)
    accessions = relationship("Accession", secondary=accession_locations_table, back_populates="locations")

    def __repr__(self) -> str:
        return f"<Location(id='{self.id}', storage_provider='{self.storage_provider}', " \
               f"storage_location='{self.storage_location}'>"


Index('location_storage', Location.storage_provider, Location.storage_location, unique=True)


def patsy_records_view_sql() -> str:
    """Returns the SQL command that creates the "patsy_records" view"""

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
                locations.storage_provider,
                locations.storage_location
                FROM batches
                LEFT JOIN accessions ON batches.id = accessions.batch_id
                LEFT JOIN accession_locations ON accessions.id = accession_locations.accession_id
                LEFT JOIN locations ON accession_locations.location_id = locations.id
                ORDER BY batches.id
    """
