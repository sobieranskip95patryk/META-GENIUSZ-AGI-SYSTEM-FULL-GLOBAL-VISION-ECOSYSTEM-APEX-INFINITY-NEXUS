from typing import Dict, Any
from .scoring import ScoringEngine
from .policy import PolicyEngine
from .execution import ExecutionRouter


class UnifiedIntelligenceEngine:
    """Enterprise-ready starter orchestrator (simplified).

    This engine wires scoring, policy and execution components and exposes
    a single async `process` API for decisioning pipelines.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.scoring = ScoringEngine(self.config.get("scoring"))
        self.policy = PolicyEngine(self.config.get("policy"))
        self.execution = ExecutionRouter(self.config.get("execution"))

    async def process(self, input_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Run the full pipeline: normalize -> score -> policy -> execute."""
        context = self._normalize(input_payload)
        prediction = await self.scoring.evaluate(context)
        governance_decision = self.policy.apply(context, prediction)
        result = await self.execution.route(governance_decision)
        return {
            "prediction": prediction,
            "decision": governance_decision,
            "execution": result,
        }

    def _normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Minimal normalization: ensure dict
        if not isinstance(payload, dict):
            return {"input": payload}
        return payload
