import types
import pytest

from spiral.pipeline.synergy_orchestrator import SynergyOrchestrator


class DummyLTM:
    def __init__(self):
        self.facts = []

    def add_fact(self, s, o, r):
        self.facts.append((s, o, r))

    def add_concept(self, nid, attributes=None):
        self.facts.append(('concept', nid, attributes or {}))


class DummySensory:
    def __init__(self, items):
        self._items = list(items)

    def drain(self):
        it = self._items
        self._items = []
        return it


class DummyChaosMapper:
    def map_chaos(self, payload):
        # simple heuristic: if payload contains an 'item', declare a knowledge gap
        if payload and payload.get('item'):
            return {'gaps': ['gap:missing-context']}
        return {}


class DummyIncorporation:
    def __init__(self):
        self.integrated = []

    def integrate_knowledge(self, payload):
        self.integrated.append(payload)
        return True


class DummyAGS:
    def __init__(self):
        # minimal state
        self.current_state = types.SimpleNamespace(coherence_p=0.5, autonomy_level=0.5)


def test_full_cycle_flow():
    ltm = DummyLTM()
    sensory = DummySensory([{'subject': 'a', 'object': 'b', 'relation': 'rel'}])
    chaos = DummyChaosMapper()
    inc = DummyIncorporation()
    ags = DummyAGS()

    orch = SynergyOrchestrator(ags=ags, ltm=ltm, chaos_mapper=chaos, sensory_buffer=sensory, incorporation_protocol=inc)

    summary = orch.initiate_evolutionary_cycle('test-trigger')

    # ensure events processed and LTM modified
    assert summary['events_processed'] >= 1
    assert len(ltm.facts) >= 1
    # incorporation should have been called for the detected gap
    assert len(inc.integrated) >= 1
    # coherence nudged upwards
    assert ags.current_state.coherence_p > 0.5
