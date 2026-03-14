import json
from openai import OpenAI
from backend.utils.prompt_templates import QA_AGENT_SYSTEM_PROMPT as qa_prompt

client = OpenAI(api_key = "FILL")

def evaluate_closed_ticket(ticket_id: str, chat_transcript: str) -> dict:
    try:
        response = client.chat.completions.create(
            model = "FILL",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": qa_prompt},
                {"role": "user", "content": f"CHAT TRANSCRIPT:\n{chat_transcript}\n\nEvaluate this."}
            ],
            temperature=0.2
        )

        raw_result = response.choices[0].message.content
        qa_report = json.loads(raw_result)

        qa_report["ticket_id"] = ticket_id

        return qa_report

    except Exception as e:
        print(f"Помилка роботи QA Agent для тікета {ticket_id}: {e}")
        return {"error": str(e)}