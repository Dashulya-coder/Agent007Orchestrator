from backend.agents.intake_agent import analyze_message
from backend.agents.routing_agent import route_request
from backend.agents.action_agent import execute_action
from backend.models.response_models import OrchestratorResponse


def process_request(request):
    intake_result = analyze_message(request.message)
    routing_result = route_request(intake_result, mode=request.mode)

    risk = intake_result.get("risk", "low")
    sentiment = intake_result.get("sentiment", "neutral")
    routing_decision = routing_result.get("routing_decision")

    if risk == "high":
        priority = "urgent"
    elif sentiment == "negative":
        priority = "high"
    else:
        priority = "medium"

    action_log = []
    final_reply = f"We received your message: {request.message}"
    is_resolved = False

    if routing_decision == "ai_auto_resolve":
        action_result = execute_action(request.user_id, intake_result)
        action_log.append({
            "action_name": action_result["action_name"],
            "status": action_result["status"],
            "details": action_result["details"]
        })
        final_reply = action_result["final_reply_to_user"] or final_reply
        is_resolved = action_result["is_resolved"]

    return OrchestratorResponse(
        case_id="case_123",
        user_id=request.user_id,
        final_reply_to_user=final_reply,
        intent=intake_result.get("intent"),
        category=intake_result.get("category"),
        priority=priority,
        sentiment=sentiment,
        routing_decision=routing_decision,
        agent_states=[],
        action_log=action_log,
        copilot=None,
        is_resolved=is_resolved
    )