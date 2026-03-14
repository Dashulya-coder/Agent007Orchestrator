import json
from backend.services.llm_client import call_llm
from backend.utils.prompt_templates import INTAKE_AGENT_SYSTEM_PROMPT


def analyze_message(message: str) -> dict:
    prompt = f"""{INTAKE_AGENT_SYSTEM_PROMPT}

User message:
{message}
"""

    response = call_llm(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "intent_clear": False,
            "intent": "unknown",
            "category": "other",
            "confidence": 0.0,
            "risk": "medium",
            "sentiment": "neutral"
        }