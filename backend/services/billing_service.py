from .mock_db import payments

def check_payment(user_id: int):

    user_pays = [p for p in payments if p["user_id"] == user_id]
    return f"Знайдено {len(user_pays)} платежів. Статус останнього: {user_pays[-1]['status'] if user_pays else 'немає'}"

def issue_refund(payment_id: str):
    
    for p in payments:
        if p["id"] == payment_id:
            p["status"] = "refunded"
            return f"Платіж {payment_id} успішно повернуто."
    return "Платіж не знайдено."