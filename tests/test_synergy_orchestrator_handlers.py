import types
import pytest

from spiral.pipeline.synergy_orchestrator import SynergyOrchestrator


class LTMSpy:
    def __init__(self):
        self.facts = []
        self.concepts = []

    def add_fact(self, s, o, r):
        self.facts.append((s, o, r))

    def add_concept(self, nid, attributes=None):
        self.concepts.append((nid, attributes or {}))

    def get_all_concepts(self):
        # represent concepts as dicts expected by ChaosMapper
        return [{'content': str(c[0])} for c in self.concepts]


class SensoryEmpty:
    def drain(self):
        return []


class SensoryConceptOnly:
    def __init__(self, items):
        self._items = list(items)

    def drain(self):
        it = self._items
        self._items = []
        return it


class ChaosNoFindings:
    def map_chaos(self, ctx):
        return {}


class IncNoop:
    def integrate_knowledge(self, payload):
        return True


class AGSDummy:
    def __init__(self):
        self.current_state = types.SimpleNamespace(coherence_p=0.2, autonomy_level=0.3)


def test_genesis_adds_concept_for_nonfact_item():
    ltm = LTMSpy()
    sensory = SensoryConceptOnly([{'id': 'concept-123'}])
    chaos = ChaosNoFindings()
    inc = IncNoop()
    ags = AGSDummy()

    orch = SynergyOrchestrator(ags=ags, ltm=ltm, chaos_mapper=chaos, sensory_buffer=sensory, incorporation_protocol=inc)

    # trigger genesis
    orch.process_event({'type': 'GenesisTriggered', 'payload': {'trigger': 't'}})

    # concept should be added to LTM (fallback path)
    assert any(c[0] == 'concept-123' for c in ltm.concepts)


def test_process_unknown_event_does_not_raise_and_ignores():
    ltm = LTMSpy()
    sensory = SensoryEmpty()
    chaos = ChaosNoFindings()
    inc = IncNoop()
    ags = AGSDummy()

    orch = SynergyOrchestrator(ags=ags, ltm=ltm, chaos_mapper=chaos, sensory_buffer=sensory, incorporation_protocol=inc)

    # processing unknown event should not raise
    orch.process_event({'type': 'UnknownEventType', 'payload': {'x': 1}})

    # queue should remain empty and LTM untouched
    assert len(ltm.facts) == 0
    assert len(ltm.concepts) == 0


def test_get_current_state_returns_ags_state():
    ltm = LTMSpy()
    sensory = SensoryEmpty()
    chaos = ChaosNoFindings()
    inc = IncNoop()
    ags = AGSDummy()

    orch = SynergyOrchestrator(ags=ags, ltm=ltm, chaos_mapper=chaos, sensory_buffer=sensory, incorporation_protocol=inc)

    state = orch.get_current_state()
    assert state is ags.current_state
