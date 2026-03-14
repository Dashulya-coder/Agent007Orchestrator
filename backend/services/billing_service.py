from .mock_db import payments

def check_payment(user_id: int):

    user_pays = [p for p in payments if p["user_id"] == user_id]
    return f"Знайдено {len(user_pays)} платежів. Статус останнього: {user_pays[-1]['status'] if user_pays else 'немає'}"

def issue_refund(payment_id: str):
    for p in payments:
        if p["id"] == payment_id:
            p["status"] = "refunded"
            user_id = p["user_id"]
            user_pays = [pay for pay in payments if pay["user_id"] == user_id]
            return {
                "status": "success",
                "payments_found": len(user_pays),
                "last_status": "refunded"
            }
    return "Платіж не знайдено."
