from backend.models.request_models import UserRequest
from backend.orchestrator import process_request


def main():
    requests = [
        UserRequest(
            user_id=1,
            message="I was charged $29 twice for my pro subscription this morning. Please refund the extra charge."
        ),
        UserRequest(
            user_id=2,
            message="Someone changed my email and password! I didn't do this and I can't access my account right now. Help!"
        ),
        UserRequest(
            user_id=3,
            message="I paid for premium yesterday, but my account is still on the free plan."
        ),
        UserRequest(
            user_id=4,
            message="I completely forgot my password and the reset link in my email is expired. Can you send a new one?"
        ),
        UserRequest(
            user_id=5,
            message="Help please"
        ),
    ]

    for i, request in enumerate(requests, start=1):
        print(f"\n--- Scenario {i} ---")
        result = process_request(request)
        print(result.model_dump(mode="json"))


if __name__ == "__main__":
    main()