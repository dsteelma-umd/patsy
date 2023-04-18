from sqlalchemy import Column, Integer, String, Index, ForeignKey, Table, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

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


class LocationsType(Base):   # type: ignore
    """Class representing ths storage providers"""

    __tablename__ = "locations_type"

    id = Column(Integer, primary_key=True)
    storage_provider = Column(String, nullable=False, unique=True)


class Location(Base):  # type: ignore
    """
    Class representing a storage location for an accession.
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    accessions = relationship("Accession", secondary=accession_locations_table, back_populates="locations")
    storage_provider_id = Column(Integer, ForeignKey('locations_type.id'))
    storage_provider = relationship("LocationsType")

    def __repr__(self) -> str:
        return f"<Location(id='{self.id}', storage_provider='{self.storage_provider_id}', " \
               f"storage_location='{self.storage_location}'>"
