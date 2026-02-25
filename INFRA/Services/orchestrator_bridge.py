"""Adapter bridge exposing Orchestrator to infra/bridge layer.

Provides a lightweight wrapper to start cycles and query state.
"""
from typing import Any, Dict


class OrchestratorBridge:
    def __init__(self, orchestrator: Any):
        self.orchestrator = orchestrator

    def start_cycle(self, trigger: str) -> Dict[str, Any]:
        """Start an evolutionary cycle and return its summary."""
        return self.orchestrator.initiate_evolutionary_cycle(trigger)

    def get_state(self) -> Any:
        """Return current orchestrator/AGS state."""
        return self.orchestrator.get_current_state()
