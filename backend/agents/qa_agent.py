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
        start = response.find("{")
        end = response.rfind("}") + 1
        json_text = response[start:end]
        return json.loads(json_text)
    except Exception:
        return {
            "issue_resolved": False,
            "csat_estimate": 3,
            "resolution_summary": "Couldn't analyze transcript",
            "improvement_insight": "QA report generation failure"
        }
