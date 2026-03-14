from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="AI Support Orchestrator")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "online"}