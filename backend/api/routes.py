from fastapi import APIRouter
from backend.models.request_models import UserRequest
from backend.models.response_models import OrchestratorResponse

router = APIRouter()

@router.post("/process", response_model=OrchestratorResponse)
async def process_request(request: UserRequest):
    # Тут пізніше буде виклик orchestrator.process(request) 
    # Поки що повертаємо мок-дані 
    return {
        "case_id": "case_123",
        "user_id": request.user_id,
        "final_reply_to_user": f"Ми отримали ваше повідомлення: {request.message}",
        "routing_decision": "ai_assist_human",
        "agent_states": [],
        "action_log": []
    }
