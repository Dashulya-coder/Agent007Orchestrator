from datetime import datetime
from .mock_db import active_cases

def append_log(case_id: str, action_name: str, status: str, details: str):
    """
    Технічна функція для фіксації дій у таймлайні кейсу.
    Додає timestamp автоматично, що потрібно для Dashboard Антона.
    """

    if case_id not in active_cases:
        return False
    
  
    new_entry = {
        "timestamp": datetime.now(),
        "action_name": action_name,
        "status": status, # 'success' або 'error'
        "details": str(details)
    }
    
    # Додаємо в масив логів конкретного кейсу 
    active_cases[case_id]["action_log"].append(new_entry)
    return True