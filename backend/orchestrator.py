from backend.agents.intake_agent import analyze_message
from backend.agents.routing_agent import route_request
from backend.models.response_models import OrchestratorResponse


def process_request(request):
    intake_result = analyze_message(request.message)
    routing_result = route_request(intake_result)

    risk = intake_result.get("risk", "low")
    sentiment = intake_result.get("sentiment", "neutral")

    if risk == "high":
        priority = "urgent"
    elif sentiment == "negative":
        priority = "high"
    else:
        priority = "medium"

    return OrchestratorResponse(
        case_id="case_123",
        user_id=request.user_id,
        final_reply_to_user=f"We received your message: {request.message}",
        intent=intake_result.get("intent"),
        category=intake_result.get("category"),
        priority=priority,
        sentiment=sentiment,
        routing_decision=routing_result.get("routing_decision"),
        agent_states=[],
        action_log=[],
        copilot=None,
        is_resolved=False
    )