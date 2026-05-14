from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.james_controller import James
from database import get_db


app = FastAPI(title="Main App")

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

@app.get("/")
def read_root():
    return {"message": "Fast API 메인페이지.", "docs": "/docs"}

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