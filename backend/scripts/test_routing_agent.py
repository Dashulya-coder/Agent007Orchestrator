from backend.agents.intake_agent import analyze_message
from backend.agents.routing_agent import route_request


def main():
    messages = [
        "I was charged $29 twice for my pro subscription this morning. Please refund the extra charge.",
        "Someone changed my email and password! I didn't do this and I can't access my account right now. Help!",
        "I paid for premium yesterday, but my account is still on the free plan.",
        "I completely forgot my password and the reset link in my email is expired. Can you send a new one?",
        "Help please",
    ]

    modes = ["conservative", "assisted", "autonomous"]

    for mode in modes:
        print(f"\n========== MODE: {mode.upper()} ==========")

        for i, message in enumerate(messages, start=1):
            print(f"\n--- Scenario {i} ---")
            print("Message:", message)

            intake_result = analyze_message(message)
            routing_result = route_request(intake_result, mode=mode)

            print("Intake result:", intake_result)
            print("Routing result:", routing_result)


if __name__ == "__main__":
    main()