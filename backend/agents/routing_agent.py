def route_request(intake_result: dict, mode: str = "assisted") -> dict:
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

    if mode == "conservative":
        if confidence >= 0.95 and intent == "password_reset":
            return {
                "routing_decision": "ai_auto_resolve",
                "reason": "Safe action in conservative mode"
            }
        return {
            "routing_decision": "ai_assist_human",
            "reason": "Conservative mode prefers human oversight"
        }

    if mode == "assisted":
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

    if mode == "autonomous":
        if confidence < 0.75:
            return {
                "routing_decision": "ai_assist_human",
                "reason": "Confidence too low even for autonomous mode"
            }

        if risk in {"low", "medium"}:
            return {
                "routing_decision": "ai_auto_resolve",
                "reason": "Autonomous mode allows low/medium-risk auto resolution"
            }

    return {
        "routing_decision": "ai_assist_human",
        "reason": "Fallback route"
    }