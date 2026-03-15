from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router

app = FastAPI(title="AI Support Orchestrator Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if (FRONTEND_DIR / "js").exists():
    app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/client_ui")
async def client_ui():
    file_path = FRONTEND_DIR / "client.html"
    return FileResponse(str(file_path))


@app.get("/worker_ui")
async def worker_ui():
    file_path = FRONTEND_DIR / "worker.html"
    return FileResponse(str(file_path))


app.include_router(router)


@app.get("/health")
def health():
    return {"status": "online"}