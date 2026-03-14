from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="AI Support Orchestrator Demo")

# Дозволяємо фронтенду вільно звертатися до бекенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтуємо статику (переконайся, що шлях до папки frontend правильний)
app.mount("/js", StaticFiles(directory="../frontend/js"), name="js")
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Роути для сторінок
@app.get("/client_ui")
async def client_ui(): return FileResponse("../frontend/client.html")

@app.get("/worker_ui")
async def worker_ui(): return FileResponse("../frontend/worker.html")

# Підключаємо роути БЕЗ Depends(get_api_key)
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "online"}