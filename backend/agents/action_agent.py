from backend.services.billing_service import check_payment, issue_refund
from backend.services.subscription_service import sync_subscription
from backend.services.mock_db import get_case
from backend.services.action_log import append_log
from backend.models.enums import RoutingDecision

from services.billing_service import check_payment, issue_refund
from services.subscription_service import sync_subscription
from services.mock_db import get_case
from services.action_log import append_log
from models.enums import RoutingDecision

async def execute_action_flow(case_id: str, action_name: str):
    case = get_case(case_id)
    if not case:
        return {"error": "Case not found"}

    result = None
    status = "success"

    try:
        if action_name == "check_payment":
            result = check_payment(case["user_id"])

        elif action_name == "issue_refund":
            payment_id = case.get("payment_id")
            if not payment_id:
                result = "Payment ID not found for refund action."
                status = "error"
            else:
                result = issue_refund(payment_id)

        elif action_name == "sync_subscription":
            result = sync_subscription(case["user_id"])

        else:
            result = f"Unknown tool: {action_name}"
            status = "error"

    except Exception as e:
        result = f"System Error: {str(e)}"
        status = "error"

    if result and ("не знайдено" in str(result).lower() or "not found" in str(result).lower() or status == "error"):
        status = "error"
        case["routing_decision"] = RoutingDecision.ESCALATE_TO_HUMAN
        case["final_reply_to_user"] = "Автоматична дія не вдалася. Передаю кейс спеціалісту."

    append_log(
        case_id=case_id,
        action_name=action_name,
        status=status,
        details=str(result)
    )

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
        "new_routing": case.get("routing_decision")
    }