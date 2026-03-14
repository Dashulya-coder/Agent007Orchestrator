from backend.agents.intake_agent import analyze_message
from backend.agents.action_agent import execute_action


def main():
    test_cases = [
        (1, "I was charged twice for my subscription."),
        (2, "I paid for premium but my account is still free."),
        (3, "My reset link expired and I need a new one."),
        (4, "Someone hacked my account."),
    ]

    for i, (user_id, message) in enumerate(test_cases, start=1):
        print(f"\n--- Scenario {i} ---")
        intake_result = analyze_message(message)
        action_result = execute_action(user_id, intake_result)
        print("Intake:", intake_result)
        print("Action:", action_result)


if __name__ == "__main__":
    main()