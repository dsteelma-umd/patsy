from patsy.alembic.patsy_record_views_sql import patsy_records_view_select
from sqlalchemy.orm import Session
from sqlalchemy.ext.compiler import compiles
from patsy.core.db_gateway import DbGateway
from sqlalchemy.schema import DropTable
from patsy.core.load import Load
from argparse import Namespace
from patsy.model import Base


# Needed when running tests against Postgres, so that dependent tables/views
# such as "patsy_record_view" don't prevent a table from being dropped.
@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def init_database(obj, addr, args=Namespace()):
    """Used in test "setUp" to initializes the database for use by tests."""
    args.database = addr
    if ((not hasattr(obj, 'gateway')) or (obj.gateway is None)):
        obj.gateway = DbGateway(args)

    session = obj.gateway.session
    engine = session.get_bind()
    Base.metadata.create_all(engine)
    drop_patsy_records_view(session)
    create_patsy_records_view(session)
    return obj


def clear_database(obj):
    """Used in test "teardown" to drop the database after tests."""
    obj.gateway.close()
    Base.metadata.drop_all(obj.gateway.session.get_bind())
    drop_patsy_records_view(obj.gateway.session)


def create_patsy_records_view(session: Session):
    sql = "CREATE VIEW patsy_records AS " + patsy_records_view_select['v2']
    session.execute(sql)


def drop_patsy_records_view(session: Session):
    session.execute("DROP VIEW IF EXISTS patsy_records;")
