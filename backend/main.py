from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

BASE_DIR = Path(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="AI Support Orchestrator Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/client_ui")
async def client_ui(): return FileResponse(str(FRONTEND_DIR / "client.html"))

@app.get("/worker_ui")
async def worker_ui(): return FileResponse(str(FRONTEND_DIR / "worker.html"))

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "online"}