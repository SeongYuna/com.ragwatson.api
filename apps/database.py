import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_BACKEND_ROOT / ".env")


def _normalize_async_db_url(url: str | None) -> str | None:
    """postgresql:// → postgresql+psycopg_async:// (이미 async 드라이버면 그대로)."""
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


# Neon DB URL 가져오기 (기본 postgresql:// 는 psycopg2로 해석되므로 비동기 URL로 바꿈)
_raw_database_url = os.getenv("DATABASE_URL")
DATABASE_URL = _normalize_async_db_url(_raw_database_url)

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL이 비어 있습니다. backend/.env에 Neon 등의 연결 문자열을 설정하세요."
    )

# 비동기 엔진 생성 (psycopg v3 async — requirements 의 psycopg[binary])
engine = create_async_engine(DATABASE_URL, echo=True)


# 세션 팩토리 생성
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


# Dependency: DB 세션 주입
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
