
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="AI Support Orchestrator PRO")

API_KEY = "skelar_hackathon_2026"
api_key_header = APIKeyHeader(name="X-API-KEY")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Усі роути захищені API ключем
app.include_router(router, dependencies=[Depends(get_api_key)])

@app.get("/health")
def health():
    return {"status": "securely online"}
