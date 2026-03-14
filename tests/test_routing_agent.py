import unittest
from backend.agents.routing_agent import route_request

class TestRoutingAgent(unittest.TestCase):

    def test_unclear_intent_asks_followup(self):
        intake = {"intent_clear": False, "intent": "unknown", "confidence": 0.4, "risk": "low"}
        result = route_request(intake)
        self.assertEqual(result["routing_decision"], "ask_follow_up")

    def test_high_risk_always_escalates(self):
        intake = {"intent_clear": True, "intent": "account_compromised", "confidence": 0.95, "risk": "high"}
        result = route_request(intake, mode="autonomous")
        self.assertEqual(result["routing_decision"], "escalate_to_human")


    def test_conservative_mode_auto_resolves_only_password(self):
        intake = {"intent_clear": True, "intent": "password_reset", "confidence": 0.98, "risk": "low"}
        result = route_request(intake, mode="conservative")
        self.assertEqual(result["routing_decision"], "ai_auto_resolve")

    def test_conservative_mode_assists_other_intents(self):
        intake = {"intent_clear": True, "intent": "duplicate_charge", "confidence": 0.99, "risk": "low"}
        result = route_request(intake, mode="conservative")
        self.assertEqual(result["routing_decision"], "ai_assist_human")


    def test_assisted_mode_auto_resolves_supported(self):
        intake = {"intent_clear": True, "intent": "duplicate_charge", "confidence": 0.90, "risk": "low"}
        result = route_request(intake, mode="assisted")
        self.assertEqual(result["routing_decision"], "ai_auto_resolve")

    def test_assisted_mode_assists_on_low_confidence(self):
        intake = {"intent_clear": True, "intent": "duplicate_charge", "confidence": 0.80, "risk": "low"}
        result = route_request(intake, mode="assisted")
        self.assertEqual(result["routing_decision"], "ai_assist_human")


    def test_autonomous_mode_resolves_medium_risk(self):
        intake = {"intent_clear": True, "intent": "refund_complaint", "confidence": 0.80, "risk": "medium"}
        result = route_request(intake, mode="autonomous")
        self.assertEqual(result["routing_decision"], "ai_auto_resolve")

if __name__ == '__main__':
    unittest.main()