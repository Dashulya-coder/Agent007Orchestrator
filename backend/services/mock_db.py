from datetime import datetime, timedelta

# Списки для імітації бази даних [cite: 401]
users = {
    1: {"id": 1, "name": "Олексій", "email": "alex@test.com", "plan": "free"},
    2: {"id": 2, "name": "Марія", "email": "maria@test.com", "plan": "premium"},
    3: {"id": 3, "name": "Андрій", "email": "cyber@secure.com", "plan": "premium"}
}

payments = [
    # Для кейсу з дублікатом [cite: 141]
    {"id": "pay_1", "user_id": 1, "amount": 10.0, "status": "success", "time": datetime.now() - timedelta(minutes=5)},
    {"id": "pay_2", "user_id": 1, "amount": 10.0, "status": "success", "time": datetime.now() - timedelta(minutes=4)},
    # Для кейсу зі збоєм підписки [cite: 142]
    {"id": "pay_3", "user_id": 2, "amount": 50.0, "status": "success", "time": datetime.now() - timedelta(days=1)}
]

subscriptions = {
    1: {"user_id": 1, "status": "inactive"}, # Має стати active після фіксу
    2: {"user_id": 2, "status": "inactive"}, # Технічний збій
}