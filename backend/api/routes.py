from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class UserRequest(BaseModel):
    user_id: int
    message: str

@router.post("/process")
async def process_request(request: UserRequest):
    
    #TODO: оркестрація
    return {
        "status": "received",
        "agent_thoughts": "Аналізую ваш запит...",
        "final_reply": f"Привіт, ми отримали ваш запит: '{request.message}'"
    }