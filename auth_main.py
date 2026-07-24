"""Auth Gateway FastAPI 앱 — auth.seongyuna.cloud 전용 엔트리포인트.

main.py(비즈니스 API)와 별도 컨테이너로 기동한다. JWT_PRIVATE_KEY는
apps/auth 내부의 발급 함수(core.security.create_access_token 등) 호출
시점에만 읽히므로, 이 파일 자체는 개인키 없이도 import된다.
"""

import sys
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent
_APPS_DIR = _BACKEND_ROOT / "apps"
for _path in (_BACKEND_ROOT, _APPS_DIR):
    _path_str = str(_path)
    if _path_str not in sys.path:
        sys.path.insert(0, _path_str)

from fastapi import FastAPI

from auth.router import router as auth_router
from core.database import init_db

app = FastAPI(
    title="RAG Tailor Auth",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.include_router(auth_router, prefix="/auth")


@app.on_event("startup")
async def on_startup() -> None:
    # auth.router → repository → models 임포트 체인으로 AuthAccountORM이 이미
    # Base.metadata에 등록된 상태 — alembic 마이그레이션을 깜빡해도 최소한
    # 테이블은 자동 생성되게 하는 안전장치 (main.py와 동일한 패턴).
    await init_db()


@app.get("/healthz")
async def healthz() -> dict:
    return {"ok": True}


if __name__ == "__main__":
    import os

    import uvicorn

    os.chdir(Path(__file__).resolve().parent)
    uvicorn.run("auth_main:app", host="127.0.0.1", port=9000, reload=True)
