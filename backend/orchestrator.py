from backend.agents.intake_agent import analyze_message
from backend.agents.routing_agent import route_request
from backend.agents.action_agent import execute_action_flow
from backend.models.response_models import OrchestratorResponse
from backend.agents.copilot_agent import generate_copilot_data


async def process_request(request):
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
    copilot_data = None

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
        action_name_map = {
            "duplicate_charge": "check_payment",
            "paid_but_not_activated": "sync_subscription",
            "password_reset": "password_reset_support",
        }

        action_name = action_name_map.get(intake_result.get("intent"), "unknown_tool")
        action_result = await execute_action_flow("CS-A1B2", action_name)

        action_log.append({
            "action_name": action_name,
            "status": action_result.get("action_status", "error"),
            "details": action_result.get("result_details", "No details")
        })

        if action_result.get("action_status") == "success":
            if action_name == "check_payment":
                final_reply = "We found your recent payment records and flagged this billing issue for resolution."
                is_resolved = True
            elif action_name == "sync_subscription":
                final_reply = "Your subscription status has been refreshed. Please check your account again."
                is_resolved = True
            elif action_name == "password_reset_support":
                final_reply = "We can help you with a new password reset flow."
                is_resolved = True
        else:
            final_reply = "We found your request, but we could not complete the action automatically."
            is_resolved = False

        agent_states.append({
            "name": "Action",
            "status": "done" if action_result.get("action_status") == "success" else "error",
            "thought": f"Executed {action_name}"
        })
        agent_states.append({
            "name": "Copilot",
            "status": "idle",
            "thought": "Not needed for auto-resolve flow"
        })

    elif routing_decision in {"ai_assist_human", "escalate_to_human"}:
        copilot_data = generate_copilot_data(
            request.message,
            f"Intent: {intake_result.get('intent')}, Category: {intake_result.get('category')}"
        )

        agent_states.append({
            "name": "Action",
            "status": "idle",
            "thought": "No automated action executed"
        })
        agent_states.append({
            "name": "Copilot",
            "status": "done",
            "thought": "Generated assistance data for human agent"
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
        copilot=copilot_data,
        is_resolved=is_resolved
    )