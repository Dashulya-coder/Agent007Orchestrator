
def route_request(intake_result: dict) -> dict:
    intent_clear = intake_result.get("intent_clear", False)
    intent = intake_result.get("intent", "other")
    confidence = intake_result.get("confidence", 0.0)
    risk = intake_result.get("risk", "medium")

    if not intent_clear:
        return {
            "routing_decision": "ask_follow_up",
            "reason": "Intent is unclear"
        }

    if risk == "high":
        return {
            "routing_decision": "escalate_to_human",
            "reason": "High-risk case"
        }

    if confidence < 0.85:
        return {
            "routing_decision": "ai_assist_human",
            "reason": "Low confidence"
        }

    if intent in {"duplicate_charge", "paid_but_not_activated", "password_reset"}:
        return {
            "routing_decision": "ai_auto_resolve",
            "reason": "Supported low-risk action"
        }

    return {
        "routing_decision": "ai_assist_human",
        "reason": "Human support recommended"
    }