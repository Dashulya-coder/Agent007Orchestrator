import json
from backend.services.llm_client import call_llm
from backend.utils.prompt_templates import QA_AGENT_SYSTEM_PROMPT


def evaluate_closed_ticket(chat_transcript: str) -> dict:
    prompt = f"""{QA_AGENT_SYSTEM_PROMPT}

    Chat Transcript:
    {chat_transcript}
    """

    response = call_llm(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "issue_resolved": False,
            "csat_estimate": 3,
            "resolution_summary": "Couldn't analyze transcript",
            "improvement_insight": "QA-report generation failure"
        }