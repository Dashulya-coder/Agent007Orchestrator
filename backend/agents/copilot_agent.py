import json
from backend.services.llm_client import call_llm
from backend.utils.prompt_templates import COPILOT_AGENT_SYSTEM_PROMPT


def generate_copilot_data(user_message: str, system_context: str) -> dict:
    prompt = f"""{COPILOT_AGENT_SYSTEM_PROMPT}

USER MESSAGE:
{user_message}

SYSTEM CONTEXT:
{system_context}
"""

    response = call_llm(prompt)

    print("RAW COPILOT RESPONSE:")
    print(response)

    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        json_text = response[start:end]
        return json.loads(json_text)
    except Exception:
        return {
            "summary": "Unable to parse copilot response",
            "probable_cause": "Unknown",
            "suggested_actions": [],
            "draft_reply": "A human agent will assist the user shortly."
        }