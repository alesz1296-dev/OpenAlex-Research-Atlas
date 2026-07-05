"""
Alembic env.py configured to use the project's SQLAlchemy models.

LEARNING: This file configures Alembic to run migrations against
the metadata exposed by `src.database.models.Base.metadata`.

It dynamically sets the SQLAlchemy URL from project settings, so you
can keep credentials out of `alembic.ini` and rely on `.env` or env vars.
"""
from __future__ import with_statement
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Ensure project root is on PYTHONPATH so imports work when running alembic
sys.path.append(os.path.abspath(os.getcwd()))

# Import project settings and metadata
try:
    from src.core.config import settings
    from src.database.models import Base
except Exception as e:
    # If imports fail, raise a helpful error
    raise ImportError(
        "Failed to import project modules. Ensure `src` is on PYTHONPATH and dependencies are installed."
    ) from e

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set SQLAlchemy URL from project settings (env/.env).
# Tests may set ALEMBIC_DATABASE_URL so migration-owned fixtures can target a
# disposable database even if application settings were imported earlier.
config.set_main_option("sqlalchemy.url", os.getenv("ALEMBIC_DATABASE_URL") or settings.DATABASE_URL)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
