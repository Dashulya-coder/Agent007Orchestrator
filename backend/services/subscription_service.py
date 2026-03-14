from .mock_db import subscriptions

def sync_subscription(user_id: int):
    
    if user_id in subscriptions:
        subscriptions[user_id]["status"] = "active"
        return f"Підписку для юзера {user_id} синхронізовано та активовано."
    return "Запис про підписку не знайдено."