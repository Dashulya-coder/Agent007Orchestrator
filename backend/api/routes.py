from fastapi import APIRouter, HTTPException
import uuid
from models.request_models import UserRequest
from models.response_models import OrchestratorResponse, CaseSummary
from services.mock_db import active_cases, save_case, get_case
from services.account_service import evaluate_security_risk

router = APIRouter()

@router.get("/cases", response_model=list[CaseSummary])
async def list_monitoring_cases():
    """Сторінка 1: Моніторинг усіх чатів"""
    return [
        {
            "case_id": c["case_id"], 
            "user_id": c["user_id"], 
            "intent": c["intent"], 
            "priority": c["priority"], 
            "status": c["status"]
        } for c in active_cases.values()
    ]

@router.post("/process", response_model=OrchestratorResponse)
async def start_new_case(request: UserRequest):
    """Створення кейсу (викликає ШІ аналіз)"""
    case_id = f"CS-{uuid.uuid4().hex[:4].upper()}"
    
    # БЕЗПЕКА: Логічний аналіз ризику 
    security_eval = evaluate_security_risk(request.user_id, request.message)
    
    new_case = {
        "case_id": case_id,
        "user_id": request.user_id,
        "final_reply_to_user": "Processing...",
        "intent": "Security Alert" if security_eval["risk"] == "high" else "Service Request",
        "priority": security_eval["priority"],
        "routing_decision": "escalate_to_human" if security_eval["risk"] == "high" else "ai_assist_human",
        "status": "open",
        "agent_states": [{"name": "Intake", "status": "done", "thought": "Analyzing intent..."}],
        "action_log": [{"timestamp": "2026-03-14T18:00:00", "action_name": "risk_check", "status": "success", "details": security_eval["risk"]}],
        "copilot": {
            "summary": request.message,
            "probable_cause": "System triggered evaluation",
            "suggested_actions": ["Verify ID", "Check History"],
            "draft_reply": "Hello, we are reviewing your request."
        }
    }
    save_case(new_case)
    return new_case

@router.get("/cases/{case_id}", response_model=OrchestratorResponse)
async def get_static_details(case_id: str):
    """Сторінка 2: Дані, що не змінюються"""
    case = get_case(case_id)
    if not case: raise HTTPException(status_code=404)
    return case

@router.post("/cases/{case_id}/action")
async def update_dynamic_parts(case_id: str, action: str):
    """Динамічне оновлення кнопок та логів без перезавантаження юзера"""
    case = get_case(case_id)
    if not case: raise HTTPException(status_code=404)
    
    case["action_log"].append({"action_name": action, "status": "success", "details": "Executed by Agent"})
    case["copilot"]["suggested_actions"] = ["Archive Case", "Send Feedback Form"]
    
    return {"action_log": case["action_log"], "new_suggestions": case["copilot"]["suggested_actions"]}
