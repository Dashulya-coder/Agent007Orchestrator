from services.action_log import append_log 
from services.mock_db import get_case
from services.billing_service import check_payment, issue_refund
from services.subscription_service import sync_subscription
from models.enums import RoutingDecision, AgentStatus

async def execute_action_flow(case_id: str, suggested_action: str):
    case = get_case(case_id)
    if not case:
        return {"error": "Case not found"}

    result = None
    status = "success"

    # 1. Виклик відповідного сервісу 
    try:
        if suggested_action == "check_payment":
            result = check_payment(case["user_id"])
        elif suggested_action == "issue_refund":
            result = issue_refund("pay_123") 
        elif suggested_action == "sync_subscription":
            result = sync_subscription(case["user_id"])
        else:
            result = f"Unknown tool: {suggested_action}"
            status = "error"
    except Exception as e:
        result = f"System Error: {str(e)}"
        status = "error"

    # 2. Реалізація FAIL FLOW 
    # Якщо дія не вдалася (наприклад, платіж не знайдено)
    if result and ("не знайдено" in str(result).lower() or status == "error"):
        status = "error"
        # Передаємо кейс людині, бо AI не впорався [cite: 132, 287-288]
        case["routing_decision"] = RoutingDecision.ESCALATE_TO_HUMAN
        case["final_reply_to_user"] = "Автоматична дія не вдалася. Передаю кейс спеціалісту."
    
    # 3. ВИКЛИК СЕРВІСУ ЛОГУВАННЯ 
    # Тепер замість ручного додавання в список, використовуємо append_log
    append_log(case_id, suggested_action, status, result)
    
    return {
        "action_status": status,
        "result_details": str(result),
        "new_routing": case["routing_decision"]
    }