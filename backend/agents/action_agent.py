# backend/agents/action_agent.py

from services.billing_service import check_payment, issue_refund
from services.subscription_service import sync_subscription
from services.mock_db import get_case
from services.action_log import append_log
from models.enums import RoutingDecision

async def execute_action_flow(case_id: str, action_name: str):
    """
    Технічне ядро Action Agent: виконує інструменти та фіксує результат [cite: 57-59, 365].
    """
    case = get_case(case_id)
    if not case:
        return {"error": "Case not found"}

    result = None
    status = "success"

    # 1. Виклик відповідного сервісу за командою [cite: 104-106, 417]
    try:
        if action_name == "check_payment":
            result = check_payment(case["user_id"])
        elif action_name == "issue_refund":
            result = issue_refund("pay_123") 
        elif action_name == "sync_subscription":
            result = sync_subscription(case["user_id"])
        else:
            result = f"Unknown tool: {action_name}"
            status = "error"
    except Exception as e:
        result = f"System Error: {str(e)}"
        status = "error"

    # 2. Реалізація FAIL FLOW: якщо дія не вдалася -> передача людині [cite: 131-132, 426]
    if result and ("не знайдено" in str(result).lower() or status == "error"):
        status = "error"
        case["routing_decision"] = RoutingDecision.ESCALATE_TO_HUMAN
        case["final_reply_to_user"] = "Автоматична дія не вдалася. Передаю кейс спеціалісту."
    
    # 3. Фіксація в Action Log (автоматично додає timestamp) 
    append_log(
        case_id=case_id,
        action_name=action_name,
        status=status,
        details=str(result)
    )
    
    return {
        "action_status": status,
        "result_details": str(result),
        "new_routing": case["routing_decision"]
    }