from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="AI Support Orchestrator")

app.include_router(router) 

@app.get("/")
def health_check():
    return {"status": "online"}