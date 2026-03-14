from datetime import datetime
from services.mock_db import get_case
from services.billing_service import check_payment, issue_refund
from services.subscription_service import sync_subscription
from models.enums import RoutingDecision, AgentStatus

async def execute_action_flow(case_id: str, suggested_action: str):
    """
    Технічне ядро Action Agent: викликає інструменти та фіксує результат.
    """
    case = get_case(case_id)
    if not case:
        return {"error": "Case not found"}

    # Початковий стан: агент почав роботу
    result = None
    status = "success"

    # 1. Виклик відповідного сервісу залежно від команди [cite: 117-124, 423]
    try:
        if suggested_action == "check_payment":
            result = check_payment(case["user_id"])
        elif suggested_action == "issue_refund":
            # Імітуємо отримання payment_id з логів або контексту
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
    if result and ("не знайдено" in str(result).lower() or status == "error"):
        status = "error"
        # Міняємо маршрут на людину, бо AI не впорався [cite: 190]
        case["routing_decision"] = RoutingDecision.ESCALATE_TO_HUMAN
        case["final_reply_to_user"] = "Автоматична дія не вдалася. Передаю кейс спеціалісту."
    
    # 3. Фіксація в Action Log 
    new_log_entry = {
        "timestamp": datetime.now(),
        "action_name": suggested_action,
        "status": status,
        "details": str(result)
    }
    case["action_log"].append(new_log_entry)
    
    # Оновлюємо статус агента для UI
    return {
        "action_status": status,
        "result_details": str(result),
        "new_routing": case["routing_decision"]
    }