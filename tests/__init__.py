from sqlalchemy.ext.compiler import compiles
from patsy.core.db_gateway import DbGateway
from sqlalchemy.schema import DropTable
from patsy.core.load import Load
from argparse import Namespace
from patsy.model import Base, patsy_records_view_sql


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
    session.execute(patsy_records_view_sql())
    return obj


def clear_database(obj):
    """Used in test "teardown" to drop the database after tests."""
    obj.gateway.close()
    Base.metadata.drop_all(obj.gateway.session.get_bind())
    obj.gateway.session.execute("DROP VIEW IF EXISTS patsy_records;")
