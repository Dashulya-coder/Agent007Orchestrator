from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from .enums import AgentStatus, RoutingDecision, Priority, Sentiment

class AgentState(BaseModel):
    """Стан конкретного агента для візуалізації на UI"""
    name: str  # Intake, Routing, Action, Copilot, QA
    status: AgentStatus
    thought: Optional[str] = Field(None, description="Reasoning: 'думки' агента в реальному часі") 

class ActionLogEntry(BaseModel):
    """Запис у таймлайні дій (Action Log)""" 

    timestamp: datetime = Field(default_factory=datetime.now)
    action_name: str  # наприклад, 'check_payment_status'
    status: str  # 'success' або 'fail'
    details: str

class CopilotData(BaseModel):
    """Дані для панелі допомоги агенту-людині""" 
    summary: str
    probable_cause: str
    suggested_actions: List[str]
    draft_reply: str

class OrchestratorResponse(BaseModel):
    """Фінальна відповідь, яку повертає API після проходження всього графу""" 

    case_id: str
    user_id: int
    
    # Дані для клієнта
    final_reply_to_user: str 
    
    # Операційні дані 
    intent: Optional[str] = None
    category: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    sentiment: Sentiment = Sentiment.NEUTRAL
    routing_decision: RoutingDecision
    
    # Стан системи для UI
    agent_states: List[AgentState] 
    action_log: List[ActionLogEntry] 
    
    # Дані Copilot (якщо route не AUTO_RESOLVE)
    copilot: Optional[CopilotData] = None
    
    # Результат аналітики (від QA Agent)
    is_resolved: bool = False 

class CaseSummary(BaseModel):
    """Легка модель для сторінки моніторингу чатів"""
    case_id: str
    user_id: int
    intent: str
    priority: str
    status: str