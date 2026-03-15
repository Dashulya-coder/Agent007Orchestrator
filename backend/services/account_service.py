from backend.services.mock_db import users
from backend.models.enums import Priority


def evaluate_security_risk(user_id: int, message: str):
    user = users.get(user_id, {})
    failed_logins = user.get("failed_logins", 0)
    msg = message.lower()

    suspicious_phrases = [
        "hack",
        "hacked",
        "stolen",
        "unauthorized",
        "someone changed my email",
        "someone changed my password",
        "злам",
    ]

    is_compromised = (
        failed_logins > 3
        or any(phrase in msg for phrase in suspicious_phrases)
    )

    return {
        "risk": "high" if is_compromised else "low",
        "priority": Priority.URGENT if is_compromised else Priority.MEDIUM
    }