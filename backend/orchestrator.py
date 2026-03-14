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

    agent_states = [
        {
            "name": "Intake",
            "status": "done",
            "thought": f"Intent classified as {intake_result.get('intent')}"
        },
        {
            "name": "Routing",
            "status": "done",
            "thought": routing_result.get("reason", "Routing completed")
        }
    ]

    if routing_decision == "ai_auto_resolve":
        action_result = execute_action(request.user_id, intake_result)

        action_log.append({
            "action_name": action_result["action_name"],
            "status": action_result["status"],
            "details": action_result["details"]
        })

        final_reply = action_result["final_reply_to_user"] or final_reply
        is_resolved = action_result["is_resolved"]

        agent_states.append({
            "name": "Action",
            "status": "done" if action_result["status"] == "success" else "error",
            "thought": f"Executed {action_result['action_name']}"
        })
        agent_states.append({
            "name": "Copilot",
            "status": "idle",
            "thought": "Not needed for auto-resolve flow"
        })

    elif routing_decision in {"ai_assist_human", "escalate_to_human"}:
        agent_states.append({
            "name": "Action",
            "status": "idle",
            "thought": "No automated action executed"
        })
        agent_states.append({
            "name": "Copilot",
            "status": "working",
            "thought": "Human support or copilot assistance needed"
        })

    else:
        agent_states.append({
            "name": "Action",
            "status": "idle",
            "thought": "Waiting for clarification"
        })
        agent_states.append({
            "name": "Copilot",
            "status": "idle",
            "thought": "Copilot not started"
        })

    return OrchestratorResponse(
        case_id="case_123",
        user_id=request.user_id,
        final_reply_to_user=final_reply,
        intent=intake_result.get("intent"),
        category=intake_result.get("category"),
        priority=priority,
        sentiment=sentiment,
        routing_decision=routing_decision,
        agent_states=agent_states,
        action_log=action_log,
        copilot=None,
        is_resolved=is_resolved
    )