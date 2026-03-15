from enum import Enum

class AIMode(str, Enum):
    CONSERVATIVE = "conservative"
    ASSISTED = "assisted"
    AUTONOMOUS = "autonomous"

class RoutingDecision(str, Enum):
    AUTO_RESOLVE = "ai_auto_resolve"
    AI_ASSIST_HUMAN = "ai_assist_human"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    ASK_FOLLOW_UP = "ask_follow_up"

class AgentStatus(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    DONE = "done"
    ERROR = "error"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"