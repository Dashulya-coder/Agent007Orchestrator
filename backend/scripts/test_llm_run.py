from backend.services.llm_client import call_llm


def main():
    prompt = "Say hello in one short sentence."

    response = call_llm(prompt)

    print("Prompt:")
    print(prompt)
    print("\nLLM response:")
    print(response)


if __name__ == "__main__":
    main()