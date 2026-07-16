from logging.config import fileConfig
import os
import sys
from pathlib import Path

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
_APPS_ROOT = _BACKEND_ROOT / "apps"
sys.path.insert(0, str(_BACKEND_ROOT))
sys.path.insert(0, str(_APPS_ROOT))

load_dotenv(_BACKEND_ROOT / ".env")

from core.database import Base  # noqa: E402
from gateway_kingdom_hearts.adapter.outbound.orm import user_orm  # noqa: F401, E402
from titanic_machine_learning.adapter.outbound.orm import BookingORM, PersonORM  # noqa: F401, E402

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _sync_database_url() -> str:
    raw = os.getenv("DATABASE_URL", "").strip()
    if not raw:
        raise RuntimeError("DATABASE_URL이 비어 있습니다. backend/.env를 확인하세요.")
    if raw.startswith("postgres://"):
        raw = "postgresql://" + raw.removeprefix("postgres://")
    raw = raw.replace("postgresql+psycopg_async://", "postgresql+psycopg://")
    raw = raw.replace("postgresql+asyncpg://", "postgresql+psycopg://")
    if raw.startswith("postgresql://"):
        raw = raw.replace("postgresql://", "postgresql+psycopg://", 1)
    return raw


config.set_main_option("sqlalchemy.url", _sync_database_url())


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
