from typing import Dict, Any


class ExecutionRouter:
    """Simple execution router stub for starter."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    async def route(self, governance_decision: Dict[str, Any]) -> Dict[str, Any]:
        # Minimal execution: return acknowledged if allowed
        if governance_decision.get("decision") == "allow":
            return {"status": "executed", "detail": "action taken"}
        return {"status": "skipped", "detail": "policy denied"}
