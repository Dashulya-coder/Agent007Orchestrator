from datetime import datetime
from backend.services.mock_db import active_cases


def append_log(case_id: str, action_name: str, status: str, details: str):
    if case_id not in active_cases:
        return False

    new_entry = {
        "timestamp": datetime.now(),
        "action_name": action_name,
        "status": status,
        "details": str(details)
    }

    active_cases[case_id]["action_log"].append(new_entry)
    return True