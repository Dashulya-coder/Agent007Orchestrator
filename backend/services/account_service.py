from .mock_db import users
from models.enums import Priority

def evaluate_security_risk(user_id: int, message: str):
    user = users.get(user_id, {"failed_logins": 0})
    msg = message.lower()
    
    # Визначаємо High Risk: підозріла активність або ключові слова [cite: 190-193]
    is_compromised = user["failed_logins"] > 3 or any(w in msg for w in ["hack", "password", "stolen", "злам"])
    
    return {
        "risk": "high" if is_compromised else "low",
        "priority": Priority.URGENT if is_compromised else Priority.MEDIUM
    }