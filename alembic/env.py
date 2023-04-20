from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# UMD Customization
from patsy.alembic.helpers.replaceable_objects import *
from patsy.database import get_database_connection_url
from patsy.model import Base
# End UMD Customization

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# UMD Customization
# target_metadata = None
target_metadata = Base.metadata
# End UMD Customization

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # UMD Customization
    # url = config.get_main_option("sqlalchemy.url")
    database_arg = config.get_main_option("database")
    database_connection_url = get_database_connection_url(database_arg)

    url = database_connection_url
    # End UMD Customization

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # UMD Customization
    database_arg = context.get_x_argument(as_dictionary=True).get('database')
    database_connection_url = get_database_connection_url(database_arg)

    ini_section = config.get_section(config.config_ini_section)
    ini_section['sqlalchemy.url'] = database_connection_url
    # End UMD Customization

    connectable = engine_from_config(
        # UMD Customization
        # config.get_section(config.config_ini_section, {}),
        ini_section,
        # End UMD Customization
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
