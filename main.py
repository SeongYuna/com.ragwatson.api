"""FastAPI 앱.

Windows + psycopg(async): ProactorEventLoop와 호환되지 않는다.
- asyncio 정책 설정(일부 경로용)
- 파일 하단에서 uvicorn이 고르는 루프 팩토리를 SelectorEventLoop로 패치(단일 워커·reload 없음 시 필요)
"""
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# backend/ · backend/apps/ 를 sys.path에 추가 (core.*, titanic_m_learning.* 등)
from pathlib import Path as _Path

_BACKEND_ROOT = _Path(__file__).resolve().parent
_APPS_DIR = _BACKEND_ROOT / "apps"
for _path in (_BACKEND_ROOT, _APPS_DIR):
    _path_str = str(_path)
    if _path_str not in sys.path:
        sys.path.insert(0, _path_str)

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging

import google.generativeai as genai
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix_API_key.app.keymaker_api import ChatRequest, keymaker
from titanic_machine_learning.adapter.inbound.api import titanic_router
from silicon_valley.adapter.inbound.api import silicon_valley_router
from lenna_vision.adapter.inbound.api import lenna_vision_router
from titanic_machine_learning.adapter.outbound.orm import BookingORM, PersonORM  # noqa: F401 — Base.metadata
from core.database import get_db, init_db
from gateway_kingdom_hearts.adapter.inbound.api.v1.user_cmd_router import user_cmd_router
from gateway_kingdom_hearts.adapter.outbound.orm import user_orm  # noqa: F401 — Base.metadata에 UserORM 등록
from weather_service import fetch_current_weather
from teaching_assistant_spoke.adapter.inbound.api.v1.email_router import router as email_router
from starcraft_hub.adapter.inbound.api.v1.classify_router import router as classify_router
from starcraft_hub.adapter.inbound.api.v1.route_router import router as route_router
from teaching_assistant_spoke.adapter.inbound.api.v1.receiver_router import router as receiver_router
from teaching_assistant_spoke.adapter.outbound.orm import received_email_orm  # noqa: F401 — Base.metadata 등록


app = FastAPI(title="Main App")

logger = logging.getLogger("uvicorn.error")


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(titanic_router, prefix="/api")
app.include_router(silicon_valley_router, prefix="/api")
app.include_router(lenna_vision_router, prefix="/api")
app.include_router(user_cmd_router)
app.include_router(email_router, prefix="/api")
app.include_router(classify_router, prefix="/api")
app.include_router(route_router, prefix="/api")
app.include_router(receiver_router, prefix="/api")


class LoginRequest(BaseModel):
    id: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Fast API 메인페이지.", "docs": "/docs"}


@app.get("/weather")
def read_weather(
    lat: float | None = Query(None, ge=-90, le=90),
    lon: float | None = Query(None, ge=-180, le=180),
):
    try:
        return fetch_current_weather(lat=lat, lon=lon)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@app.post("/chat")
def chat(req: ChatRequest):
    if not keymaker.gemini_api_key:
        raise HTTPException(
            status_code=503,
            detail="Gemini API 키가 비어 있습니다. backend/.env에 GEMINI_API_KEY를 설정하세요.",
        )

    genai.configure(api_key=keymaker.gemini_api_key)

    msgs = req.messages
    if msgs[-1].role.lower() != "user":
        raise HTTPException(
            status_code=400,
            detail="messages의 마지막 항목은 role이 user여야 합니다.",
        )

    history: list[dict] = []
    for m in msgs[:-1]:
        r = m.role.lower()
        if r not in ("user", "assistant", "model"):
            raise HTTPException(
                status_code=400,
                detail="role은 user, assistant, model 중 하나여야 합니다.",
            )
        role = "user" if r == "user" else "model"
        history.append({"role": role, "parts": [m.content]})

    model_name = (req.model or "").strip() or keymaker.gemini_model_name

    try:
        model = genai.GenerativeModel(model_name)
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(msgs[-1].content)
        text = (response.text or "").strip()
        if not text:
            raise HTTPException(
                status_code=502,
                detail="모델이 비어 있는 응답을 반환했습니다.",
            )
        return {"reply": text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@app.post("/login")
def login(req: LoginRequest):
    logger.info("[login] 요청 — userId=%s", req.id)
    return {"ok": True, "data": req.model_dump()}


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT NOW();"))
        now = result.scalar()
        return {"status": "success", "neon_time": now}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- Windows: uvicorn이 단일 프로세스에서 ProactorEventLoop를 쓰면 psycopg async가 실패한다. ---
# get_loop_factory() 호출 시점 이전에 모듈이 로드되므로, import 직후 패치한다.
if sys.platform == "win32": 
    try:
        import uvicorn.loops.asyncio as _uvicorn_loops_asyncio

        def _asyncio_loop_factory_win_psycopg(
            use_subprocess: bool = False,
        ) -> type[asyncio.AbstractEventLoop]:
            _ = use_subprocess
            return asyncio.SelectorEventLoop

        _uvicorn_loops_asyncio.asyncio_loop_factory = _asyncio_loop_factory_win_psycopg  # type: ignore[method-assign]
    except ImportError:
        pass


if __name__ == "__main__":
    import os
    import uvicorn

    os.chdir(Path(__file__).resolve().parent)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)