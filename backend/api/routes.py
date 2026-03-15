from fastapi import APIRouter, HTTPException
from backend.models.request_models import UserRequest
from backend.models.response_models import OrchestratorResponse, CaseSummary
from backend.orchestrator import process_request
from backend.services.mock_db import active_cases, get_case
from backend.agents.action_agent import execute_action_flow

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
async def process_user_request(request: UserRequest):
    return await process_request(request)


@router.get("/active")
async def get_active_case_key():
    for cid, case in active_cases.items():
        if case.get("routing_decision") in ["escalate_to_human", "ai_assist_human"]:
            return {"key": cid}
    return None


@router.get("/cases", response_model=list[CaseSummary])
async def list_monitoring_cases():
    return [
        {
            "case_id": c["case_id"],
            "user_id": c["user_id"],
            "intent": c.get("intent", "unknown"),
            "priority": str(c.get("priority", "medium")),
            "status": c.get("status", "open"),
        }
        for c in active_cases.values()
    ]


@router.get("/cases/{case_id}")
async def get_case_details(case_id: str):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    copilot = case.get("copilot") or {}

    return {
        "case_id": case_id,
        "messages": case.get("messages", []),
        "suggestions": copilot.get("suggested_actions", []),
        "summary": {
            "summaryText": copilot.get("summary", ""),
            "priority": str(case.get("priority", "medium")),
            "tags": [case.get("intent", "general")],
        },
        "clientInfo": {
            "name": f"User {case.get('user_id')}",
            "clientId": str(case.get("user_id")),
            "lastPayment": "2026-03-10",
            "dues": "$0.00",
        },
    }


@router.post("/cases/{case_id}/active")
async def update_case_from_worker(case_id: str, payload: dict):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    case["messages"] = payload.get("messages", case.get("messages", []))
    copilot = case.get("copilot") or {}

    return {
        "case_id": case_id,
        "messages": case["messages"],
        "suggestions": copilot.get("suggested_actions", []),
        "summary": {
            "summaryText": copilot.get("summary", ""),
            "priority": str(case.get("priority", "medium")),
            "tags": [case.get("intent", "general")],
        },
        "clientInfo": {
            "name": f"User {case.get('user_id')}",
            "clientId": str(case.get("user_id")),
        },
    }


@router.post("/cases/{case_id}/action")
async def handle_action(case_id: str, action: str):
    result = await execute_action_flow(case_id, action)
    case = get_case(case_id)

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    return {
        "action_result": result,
        "action_log": case.get("action_log", []),
        "new_suggestions": ["Archive Case", "Notify User"],
    }