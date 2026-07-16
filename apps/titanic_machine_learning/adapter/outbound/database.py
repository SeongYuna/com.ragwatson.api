"""타이타닉 전용 DB 엔진.

core.database(DATABASE_URL)는 다른 앱들이 쓰는 로컬 pgvector 컨테이너를 가리킨다.
타이타닉 데이터는 Neon에만 존재하므로, 이 앱만 별도의 TITANIC_DATABASE_URL로
접속한다. ORM 선언은 core.database.Base를 그대로 재사용해 Alembic 메타데이터는
하나로 유지한다.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

_BACKEND_ROOT = Path(__file__).resolve().parents[4]
load_dotenv(_BACKEND_ROOT / ".env")


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


_raw_titanic_database_url = os.getenv("TITANIC_DATABASE_URL")
TITANIC_DATABASE_URL = _normalize_async_db_url(_raw_titanic_database_url)

if not TITANIC_DATABASE_URL:
    raise RuntimeError(
        "TITANIC_DATABASE_URL이 비어 있습니다. backend/.env에 Neon PostgreSQL 연결 문자열을 설정하세요."
    )

titanic_engine = create_async_engine(TITANIC_DATABASE_URL, echo=False, pool_pre_ping=True)

titanic_async_session = async_sessionmaker(titanic_engine, expire_on_commit=False)


async def get_titanic_db():
    async with titanic_async_session() as session:
        yield session
