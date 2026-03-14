from backend.services.billing_service import check_payment
from backend.services.subscription_service import sync_subscription


def execute_action(user_id: int, intake_result: dict) -> dict:
    intent = intake_result.get("intent", "other")

    if intent == "duplicate_charge":
        result = check_payment(user_id)
        return {
            "action_name": "check_payment",
            "status": "success",
            "details": result,
            "is_resolved": True,
            "final_reply_to_user": "We found your recent payment records and flagged this billing issue for resolution."
        }

    if intent == "paid_but_not_activated":
        result = sync_subscription(user_id)

        if "не знайдено" in result.lower():
            return {
                "action_name": "sync_subscription",
                "status": "fail",
                "details": result,
                "is_resolved": False,
                "final_reply_to_user": "We found your request, but we could not automatically update the subscription status."
            }

        return {
            "action_name": "sync_subscription",
            "status": "success",
            "details": result,
            "is_resolved": True,
            "final_reply_to_user": "Your subscription status has been refreshed. Please check your account again."
        }

    if intent == "password_reset":
        return {
            "action_name": "password_reset_support",
            "status": "success",
            "details": "Password reset guidance prepared.",
            "is_resolved": True,
            "final_reply_to_user": "We can help you with a new password reset flow."
        }

    return {
        "action_name": "no_action",
        "status": "skipped",
        "details": "No automated action available.",
        "is_resolved": False,
        "final_reply_to_user": None
    }