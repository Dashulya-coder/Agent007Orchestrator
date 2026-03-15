from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .enums import AgentStatus, RoutingDecision, Priority, Sentiment


class AgentState(BaseModel):
    name: str
    status: AgentStatus
    thought: Optional[str] = Field(None, description="Agent reasoning or current status")


class ActionLogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    action_name: str
    status: str
    details: str


class CopilotData(BaseModel):
    summary: str
    probable_cause: str
    suggested_actions: List[str]
    draft_reply: str


class OrchestratorResponse(BaseModel):
    case_id: str
    user_id: int
    final_reply_to_user: str
    intent: Optional[str] = None
    category: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    sentiment: Sentiment = Sentiment.NEUTRAL
    routing_decision: RoutingDecision
    agent_states: List[AgentState]
    action_log: List[ActionLogEntry]
    copilot: Optional[CopilotData] = None
    is_resolved: bool = False


class CaseSummary(BaseModel):
    case_id: str
    user_id: int
    intent: str
    priority: str
    status: str