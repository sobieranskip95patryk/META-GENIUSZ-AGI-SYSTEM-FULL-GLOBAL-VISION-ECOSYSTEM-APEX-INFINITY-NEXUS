"""Synergy Orchestrator (adapter of SpiralMind Orchestrator)

This file adapts the lightweight SpiralMind orchestrator implementation
to the canonical `SpiralMind Nexus v0.2.0` package layout under `spiral/pipeline`.
The class `SynergyOrchestrator` preserves the event-driven skeleton and
integrates with existing `CORE/*` stubs (SensoryBuffer, ChaosMapper, IncorporationProtocol).
"""
from collections import deque
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class SynergyOrchestrator:
    """Event-driven orchestrator for evolutionary cycles (lightweight).

    This mirrors the earlier `SpiralMindOrchestrator` implementation but
    follows the `spiral.pipeline` package layout and exposes the
    `SynergyOrchestrator` symbol expected by SpiralMind Nexus.
    """

    def __init__(
        self,
        ags: Any,
        ltm: Any,
        chaos_mapper: Any,
        sensory_buffer: Any,
        incorporation_protocol: Any,
    ):
        self.ags = ags
        self.ltm = ltm
        self.chaos_mapper = chaos_mapper
        self.sensory_buffer = sensory_buffer
        self.incorporation_protocol = incorporation_protocol

        self.event_queue = deque()

    def initiate_evolutionary_cycle(self, initial_trigger: str) -> Dict[str, Any]:
        """Start a full evolutionary cycle with an initial trigger string.

        Returns a summary dict with final state and events processed.
        """
        # enqueue initial genesis event
        self.event_queue.append({"type": "GenesisTriggered", "payload": {"trigger": initial_trigger}})

        processed = []

        while self.event_queue:
            event = self.event_queue.popleft()
            try:
                self.process_event(event)
                processed.append(event)
            except Exception as e:
                logger.exception("Failed to process event: %s", e)

        # produce a minimal summary
        final_state = getattr(self.ags, 'current_state', None)
        return {"final_state": final_state, "events_processed": len(processed)}

    def process_event(self, event: Dict[str, Any]) -> None:
        """Dispatch incoming event to the proper handler."""
        etype = event.get("type")
        payload = event.get("payload", {})

        if etype == "GenesisTriggered":
            self._handle_genesis_phase(payload)
        elif etype == "NewFactDiscovered":
            self._handle_chaos_map_phase(payload)
        elif etype == "ChaosDetected":
            self._handle_ingestion_phase(payload)
        elif etype == "KnowledgeGapIdentified":
            # for now treat as ingestion work
            self._handle_ingestion_phase(payload)
        else:
            logger.debug("Unknown event type: %s", etype)

    def get_current_state(self) -> Optional[Any]:
        return getattr(self.ags, 'current_state', None)

    # -------------------- Phase Handlers --------------------
    def _handle_genesis_phase(self, event_data: Dict[str, Any]) -> None:
        """Genesis: ingest new sensory data into LTM and emit NewFactDiscovered."""
        trigger = event_data.get("trigger")
        logger.info("[Orch/Genesis] Triggered: %s", trigger)

        # pull from sensory buffer (if available)
        try:
            new_items = []
            if hasattr(self.sensory_buffer, 'drain'):
                new_items = self.sensory_buffer.drain() or []
            elif hasattr(self.sensory_buffer, 'get_recent'):
                new_items = self.sensory_buffer.get_recent() or []

            for item in new_items:
                # normalize and add to LTM (minimal contract)
                if isinstance(item, dict) and 'subject' in item and 'object' in item and 'relation' in item:
                    self.ltm.add_fact(item['subject'], item['object'], item['relation'])
                else:
                    # fallback: add as concept
                    nid = item.get('id') if isinstance(item, dict) else str(item)
                    self.ltm.add_concept(nid, attributes={'source': 'sensory'})

                # emit NewFactDiscovered for each item
                self.event_queue.append({"type": "NewFactDiscovered", "payload": {"item": item}})

        except Exception:
            logger.exception("Error in genesis phase")

    def _handle_chaos_map_phase(self, event_data: Dict[str, Any]) -> None:
        """Chaos Map: analyze LTM for inconsistencies and emit ingestion events."""
        logger.info("[Orch/ChaosMap] Analyzing new fact(s)")
        try:
            # delegate to chaos_mapper
            result = self.chaos_mapper.map_chaos(event_data)
            # Expected result: dict with keys like 'gaps', 'contradictions'
            gaps = result.get('gaps') if isinstance(result, dict) else None
            contradictions = result.get('contradictions') if isinstance(result, dict) else None

            if gaps:
                for g in gaps:
                    self.event_queue.append({"type": "KnowledgeGapIdentified", "payload": {"gap": g}})

            if contradictions:
                for c in contradictions:
                    self.event_queue.append({"type": "ChaosDetected", "payload": {"contradiction": c}})

        except Exception:
            logger.exception("Error in chaos map phase")

    def _handle_ingestion_phase(self, event_data: Dict[str, Any]) -> None:
        """Ingestion: attempt to resolve gaps/contradictions via incorporation protocol."""
        logger.info("[Orch/Ingestion] Resolving: %s", event_data)
        try:
            success = self.incorporation_protocol.integrate_knowledge(event_data)
            # On success, optionally nudge AGS state coherence
            if success and hasattr(self.ags, 'current_state'):
                cs = self.ags.current_state
                try:
                    cs.coherence_p = min(1.0, cs.coherence_p + 0.05)
                except Exception:
                    pass
        except Exception:
            logger.exception("Error in ingestion phase")
