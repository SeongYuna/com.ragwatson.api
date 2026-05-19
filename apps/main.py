from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging
import sys

import google.generativeai as genai
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from matrix.app.keymaker import ChatRequest, keymaker
from titanic.app.james_controller import James
from database import get_db, init_db
from secom.app.models import user_model  # noqa: F401 — Base.metadata에 User 등록
from weather_service import fetch_current_weather
from secom.app.schemas.user_schema import UserSchema, UserLoginSchema
from secom.app.controllers.user_controller import UserController


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

_TITANIC_CSV_PATH = (
    Path(__file__).resolve().parent / "titanic" / "app" / "titanic_dataset.csv"
)


class LoginRequest(BaseModel):
    id: str
    password: str


class SignupRequest(BaseModel):
    id: str
    password: str
    nickname: str
    email: str

@app.post("/signup")
async def signup(req: SignupRequest, db: AsyncSession = Depends(get_db)):
    user_schema = UserSchema(
        id=req.id,
        password=req.password,
        nickname=req.nickname,
        email=req.email,
        role="user",
    )
    try:
        await UserController().save_user(db, user_schema)
    except ValueError as e:
        msg = str(e)
        if msg == "duplicate":
            raise HTTPException(
                status_code=409,
                detail="이미 존재하는 아이디 또는 이메일입니다.",
            ) from e
        if msg == "schema":
            raise HTTPException(
                status_code=500,
                detail="DB 테이블 스키마가 맞지 않습니다. 서버를 재시작해 주세요.",
            ) from e
        raise HTTPException(status_code=500, detail=msg) from e
    return {"ok": True, "data": user_schema.model_dump()}

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

@app.get("/titanic/data")
def read_titanic_data():
    james = James()
    df = james.get_data()

    return df.to_dict(orient="records")

@app.get("/titanic/count")
def read_titanic_count():
    james = James()
    count = james.get_count()

    return {"count": count}

@app.get("/titanic/count/survived")
def read_titanic_survived_count():
    james = James()
    count = james.get_survived_count()

    return {"count": count}

@app.get("/titanic/count/dead")
def read_titanic_dead_count():
    james = James()
    count = james.get_dead_count()

    return {"count": count}

@app.get("/titanic/tree")
def read_titanic_tree():
    james = James()
    tree = james.has_decision_tree_model()

    return {"tree": tree}

@app.post("/titanic/tree/train")
def train_titanic_tree():
    james = James()
    model_path = james.train_decision_tree_model()

    return {"trained": True, "model_path": model_path}


@app.get("/titanic/model")
def read_titanic_model():
    james = James()
    return {"model": james.get_current_model_name()}

@app.post("/titanic/upload")
async def upload_titanic_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    _TITANIC_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    contents = await file.read()
    _TITANIC_CSV_PATH.write_bytes(contents)

    return {
        "filename": file.filename,
        "saved_path": str(_TITANIC_CSV_PATH),
        "size": len(contents),
    }

@app.get("/doro/data")
def read_doro_data():
    doro_director = DoroDirector()
    df = doro_director.get_data()

    return df.to_dict(orient="records")

if __name__ == "__main__":
    import os
    import uvicorn

    os.chdir(Path(__file__).resolve().parent)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)