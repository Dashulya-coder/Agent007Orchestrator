from datetime import datetime

users = {
    1: {"id": 1, "name": "Олексій", "failed_logins": 0},
    2: {"id": 2, "name": "Марія", "failed_logins": 0},
    3: {"id": 3, "name": "Андрій", "failed_logins": 5}
}

subscriptions = {
    1: {"user_id": 1, "status": "inactive"},
    2: {"user_id": 2, "status": "inactive"},
    3: {"user_id": 3, "status": "premium"}
}

payments = [
    {"id": "pay_123", "user_id": 1, "amount": 29.0, "status": "success"},
    {"id": "pay_124", "user_id": 1, "amount": 29.0, "status": "success"},
    {"id": "pay_999", "user_id": 3, "amount": 100.0, "status": "failed"}
]

active_cases = {
    "CS-A1B2": {
        "case_id": "CS-A1B2",
        "user_id": 3,
        "messages": [
            {"role": "client", "name": "Андрій", "text": "Мій акаунт зламали!"}
        ],
        "final_reply_to_user": "Security check required",
        "intent": "account_compromised",
        "priority": "urgent",
        "status": "open",
        "routing_decision": "escalate_to_human",
        "agent_states": [],
        "action_log": [],
        "copilot": {
            "summary": "User reports unauthorized access.",
            "probable_cause": "Multiple failed logins detected.",
            "suggested_actions": ["check_payment", "sync_subscription"],
            "draft_reply": "We detected suspicious activity and are reviewing the case."
        }
    }
}


def save_case(data):
    active_cases[data["case_id"]] = data


def get_case(case_id):
    return active_cases.get(case_id)