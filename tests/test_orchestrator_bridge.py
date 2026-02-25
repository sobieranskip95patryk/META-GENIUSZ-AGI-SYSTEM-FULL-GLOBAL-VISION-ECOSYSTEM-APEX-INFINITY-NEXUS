import types

from INFRA.Services.orchestrator_bridge import OrchestratorBridge


class DummyOrch:
    def __init__(self):
        self.current_state = types.SimpleNamespace(coherence_p=0.6)
        self.started = False

    def initiate_evolutionary_cycle(self, trigger: str):
        self.started = True
        return {"trigger": trigger, "events_processed": 1, "final_state": self.current_state}

    def get_current_state(self):
        return self.current_state


def test_orchestrator_bridge_start_and_state():
    orch = DummyOrch()
    bridge = OrchestratorBridge(orch)

    summary = bridge.start_cycle('unit-trigger')
    assert summary['trigger'] == 'unit-trigger'
    assert orch.started

    state = bridge.get_state()
    assert state is orch.current_state
    assert state.coherence_p == 0.6
