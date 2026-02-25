from typing import Dict, Any


class PolicyEngine:
    """Simple policy engine stub for starter."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def apply(self, context: Dict[str, Any], prediction: Dict[str, Any]) -> Dict[str, Any]:
        # Minimal governance: allow if confidence > threshold
        threshold = float(self.config.get("confidence_threshold", 0.5))
        decision = "allow" if prediction.get("confidence", 0.0) >= threshold else "deny"
        return {"decision": decision, "threshold": threshold}
