from fastapi import APIRouter, HTTPException
import uuid
import random
from datetime import datetime
from models.request_models import UserRequest
from models.response_models import OrchestratorResponse, CaseSummary, AgentState, ActionLogEntry
from models.enums import AgentStatus, RoutingDecision
from services.mock_db import active_cases, save_case, get_case, users
from services.account_service import evaluate_security_risk
from agents.action_agent import execute_action_flow

router = APIRouter()

# Мокові відповіді клієнта залежно від останнього повідомлення воркера
CLIENT_REPLIES = [
    "Дякую, зрозумів. Що мені робити далі?",
    "Окей, я спробую. Скільки часу це займе?",
    "Добре, але у мене ще є питання...",
    "Чудово! Це вирішило мою проблему.",
    "Не зовсім розумію, можете пояснити детальніше?",
    "Дякую за допомогу! Коли це буде виправлено?",
    "Зрозумів, спробую зараз.",
]

# Мокові пропозиції після відповіді воркера
SUGGESTION_POOL = [
    ["verify_identity", "reset_password", "check_payment"],
    ["sync_subscription", "refund_payment", "escalate_to_manager"],
    ["archive_case", "notify_user", "check_payment"],
    ["send_instructions", "verify_email", "sync_subscription"],
    ["close_case", "follow_up_email", "escalate_to_manager"],
]

@router.get("/active")
async def get_active_case_key():
    for cid, case in active_cases.items():
        if case["routing_decision"] in [RoutingDecision.ESCALATE_TO_HUMAN, RoutingDecision.AI_ASSIST_HUMAN]:
            return {"key": cid}
    return {}

@router.post("/process", response_model=OrchestratorResponse)
async def start_new_case(request: UserRequest):
    case_id = f"CS-{uuid.uuid4().hex[:4].upper()}"
    security_eval = evaluate_security_risk(request.user_id, request.message)
    
    new_case = {
        "case_id": case_id,
        "user_id": request.user_id,
        "messages": [{"role": "client", "name": "Customer", "text": request.message}],
        "final_reply_to_user": "Обробка...",
        "intent": "Service Request",
        "priority": security_eval["priority"],
        "routing_decision": RoutingDecision.ESCALATE_TO_HUMAN if security_eval["risk"] == "high" else RoutingDecision.AI_ASSIST_HUMAN,
        "status": "open",
        "agent_states": [{"name": "Intake", "status": AgentStatus.DONE, "thought": "Analyzing..."}],
        "action_log": [{"timestamp": datetime.now(), "action_name": "risk_check", "status": "success", "details": security_eval["risk"]}],
        "copilot": {
            "summary": request.message,
            "probable_cause": "Initial analysis",
            "suggested_actions": ["check_payment", "sync_subscription"],
            "draft_reply": "Вітаю!"
        }
    }
    save_case(new_case)
    return new_case

@router.get("/cases/{case_id}")
async def get_case_details(case_id: str):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return {
        "case_id": case_id,
        "messages": case.get("messages", []),
        "suggestions": case.get("copilot", {}).get("suggested_actions", []),
        "summary": {
            "summaryText": case.get("copilot", {}).get("summary", ""),
            "priority": case.get("priority", "medium"),
            "tags": [case.get("intent", "general")]
        },
        "clientInfo": {
            "name": f"User {case.get('user_id')}",
            "clientId": str(case.get("user_id")),
            "lastPayment": "2026-03-10",
            "dues": "$0.00"
        }
    }

@router.post("/cases/{case_id}/active")
async def update_case_from_worker(case_id: str, payload: dict):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404)

    messages = payload.get("messages", [])

    # Перевіряємо що останнє повідомлення від воркера — тоді додаємо мокову відповідь клієнта
    if messages and messages[-1].get("role") == "worker":
        client_name = users.get(case.get("user_id"), {}).get("name", "Client")
        mock_reply = {
            "role": "client",
            "name": client_name,
            "text": random.choice(CLIENT_REPLIES)
        }
        messages.append(mock_reply)

    case["messages"] = messages

    # Оновлюємо пропозиції на нові випадкові
    new_suggestions = random.choice(SUGGESTION_POOL)
    case["copilot"]["suggested_actions"] = new_suggestions

    save_case(case)

    return {
        "case_id": case_id,
        "messages": case["messages"],
        "suggestions": new_suggestions,
        "summary": {
            "summaryText": case.get("copilot", {}).get("summary", ""),
            "priority": case.get("priority", "medium"),
            "tags": [case.get("intent", "general")]
        },
        "clientInfo": {
            "name": f"User {case.get('user_id')}",
            "clientId": str(case.get("user_id"))
        }
    }

@router.post("/cases/{case_id}/action")
async def handle_action(case_id: str, action: str):
    result = await execute_action_flow(case_id, action)
    case = get_case(case_id)
    return {"action_log": case["action_log"], "new_suggestions": ["Archive Case", "Notify User"]}