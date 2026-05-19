import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_BACKEND_ROOT / ".env")

# users 테이블에 있어야 하는 컬럼 (varchar/text)
_REQUIRED_USER_COLUMNS = frozenset({"id", "password", "nickname", "email", "role"})


def _normalize_async_db_url(url: str | None) -> str | None:
    """postgresql:// → postgresql+psycopg_async:// (Neon 등, 이미 async면 그대로)."""
    if not url or not (u := url.strip()):
        return url
    if u.startswith("postgres://"):
        u = "postgresql://" + u.removeprefix("postgres://")
    scheme = u.split("://", 1)[0]
    if "+psycopg_async" in scheme or "+asyncpg" in scheme:
        return u
    if scheme.startswith("postgresql+psycopg") and "+psycopg_async" not in scheme:
        return "postgresql+psycopg_async://" + u.split("://", 1)[1]
    if scheme == "postgresql":
        return "postgresql+psycopg_async://" + u.split("://", 1)[1]
    return u


_raw_database_url = os.getenv("DATABASE_URL")
DATABASE_URL = _normalize_async_db_url(_raw_database_url)

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL이 비어 있습니다. backend/.env에 Neon PostgreSQL 연결 문자열을 설정하세요."
    )


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)

# 기존 import 호환
AsyncSessionLocal = async_session


async def _fetch_users_column_types(conn) -> dict[str, str]:
    result = await conn.execute(
        text(
            """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = 'users'
            """
        )
    )
    return {row[0]: row[1] for row in result}


def _users_schema_matches(cols: dict[str, str]) -> bool:
    if not cols:
        return True
    if set(cols) != _REQUIRED_USER_COLUMNS:
        return False
    for dtype in cols.values():
        if dtype not in ("character varying", "text"):
            return False
    return True


async def init_db() -> None:
    """테이블 생성. 예전 스키마(name/age, integer id 등)면 users 를 재생성."""
    async with engine.begin() as conn:
        cols = await _fetch_users_column_types(conn)
        if cols and not _users_schema_matches(cols):
            logger.warning(
                "users 테이블 스키마 불일치 → DROP 후 재생성. 기존 컬럼: %s",
                cols,
            )
            await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))

        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session
