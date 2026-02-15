"""
ORCHESTRATOR v2.0 Bridge
=========================

Warstwa mostowa między main_orchestrator_v2.py (legacy) a orchestrator_v2.py (new).
Bezpieczna integracja bez modyfikacji istniejącego kodu.

Wersja: 1.0
Data: 2026-02-03
"""

import sys
import os

# Dodaj CORE do path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import Dict, Any, List, Optional
import logging

# Import legacy orchestrator
try:
    from CORE.main_orchestrator_v2 import CentralOrchestratorV2 as LegacyOrchestrator, IntentMessage
    LEGACY_AVAILABLE = True
except ImportError:
    LEGACY_AVAILABLE = False
    LegacyOrchestrator = None
    IntentMessage = None

# Import new orchestrator
try:
    from CORE.orchestrator_v2 import OrchestratorV2 as NewOrchestrator, IntentVector
    from CORE.integration_layer import UnifiedOrchestrator
    NEW_AVAILABLE = True
except ImportError:
    NEW_AVAILABLE = False
    NewOrchestrator = None
    IntentVector = None
    UnifiedOrchestrator = None

logger = logging.getLogger(__name__)


class OrchestratorBridge:
    """
    Most między legacy a new orchestrator.
    
    Funkcje:
        - Automatyczne przełączanie między trybami
        - Konwersja formatów danych
        - Agregacja wyników
        - Fallback do legacy jeśli new nie jest dostępny
    """
    
    def __init__(
        self,
        architect_id: str = "PATRYK_SOBIERANSKI_PM",
        prefer_new: bool = True
    ):
        """
        Args:
            architect_id: ID architekta
            prefer_new: Preferuj nowy orchestrator jeśli dostępny
        """
        self.architect_id = architect_id
        self.prefer_new = prefer_new
        
        # Inicjalizacja orchestratorów
        self.legacy = None
        self.new = None
        self.unified = None
        
        if LEGACY_AVAILABLE:
            self.legacy = LegacyOrchestrator(architect_id=architect_id)
            logger.info("[BRIDGE] Legacy orchestrator loaded")
        
        if NEW_AVAILABLE:
            self.new = NewOrchestrator(
                asqk_7g_enabled=True,
                asqk_meta_enabled=True,
                inference_enabled=True
            )
            self.unified = UnifiedOrchestrator(
                asqk_7g_enabled=True,
                asqk_meta_enabled=True,
                globalvision_enabled=True,
                inference_enabled=True
            )
            logger.info("[BRIDGE] New orchestrator v2.0 loaded")
        
        # Wybór aktywnego trybu
        self.active_mode = self._select_active_mode()
        logger.info(f"[BRIDGE] Active mode: {self.active_mode}")
    
    def _select_active_mode(self) -> str:
        """Wybierz aktywny tryb działania."""
        if self.prefer_new and NEW_AVAILABLE:
            return "NEW"
        elif LEGACY_AVAILABLE:
            return "LEGACY"
        elif NEW_AVAILABLE:
            return "NEW"
        else:
            return "NONE"
    
    def process_intent(
        self,
        intent_text: str,
        context: Optional[Dict[str, Any]] = None,
        embeddings: Optional[List[float]] = None,
        context_vectors: Optional[List[List[float]]] = None,
        priority: float = 1.0
    ) -> Dict[str, Any]:
        """
        Przetwarzanie intencji przez aktywny orchestrator.
        
        Args:
            intent_text: Tekst intencji
            context: Kontekst dodatkowy
            embeddings: Embedding intencji
            context_vectors: Wektory kontekstowe
            priority: Priorytet (0-1)
        
        Returns:
            Dict z wynikami przetwarzania
        """
        context = context or {}
        
        if self.active_mode == "NEW" and self.new:
            return self._process_new(
                intent_text, context, embeddings, context_vectors, priority
            )
        elif self.active_mode == "LEGACY" and self.legacy:
            return self._process_legacy(intent_text, context, priority)
        else:
            return {"error": "No orchestrator available", "status": "ERROR"}
    
    def _process_new(
        self,
        intent_text: str,
        context: Dict,
        embeddings: Optional[List[float]],
        context_vectors: Optional[List[List[float]]],
        priority: float
    ) -> Dict[str, Any]:
        """Przetwarzanie przez nowy orchestrator."""
        intent = IntentVector(
            intent_id=f"INTENT-{int(context.get('timestamp', 0))}",
            intent_text=intent_text,
            intent_embedding=embeddings or [],
            context=context,
            priority=priority
        )
        
        response = self.new.process_intent(
            intent=intent,
            context_vectors=context_vectors,
            adaptive_mode=True
        )
        
        return {
            "mode": "NEW_ORCHESTRATOR_V2",
            "intent_id": response.intent_id,
            "status": response.status,
            "synthesis_score": response.synthesis_result.score if response.synthesis_result else 0.0,
            "meta_score": response.meta_synthesis_result.meta_score if response.meta_synthesis_result else 0.0,
            "global_vision_score": response.global_vision_score,
            "action_vector": response.action_vector,
            "recommendations": response.recommendations,
            "execution_time_ms": response.execution_time_ms
        }
    
    def _process_legacy(
        self,
        intent_text: str,
        context: Dict,
        priority: float
    ) -> Dict[str, Any]:
        """Przetwarzanie przez legacy orchestrator."""
        intent_message = IntentMessage(
            text=intent_text,
            architect_id=self.architect_id,
            context=context,
            priority=int(priority)
        )
        
        cycle = self.legacy.execute_asqk_cycle(intent_message)
        
        return {
            "mode": "LEGACY_ORCHESTRATOR",
            "cycle_id": cycle.cycle_id,
            "status": "SUCCESS",
            "growth_magnitude": cycle.quantization_state.growth_magnitude,
            "c_cd_reduction": cycle.optimization_state.c_cd_reduction,
            "delta_stabilized": cycle.optimization_state.delta_stabilized,
            "gok_response": cycle.gok_response
        }
    
    def process_projectvector(
        self,
        project_vector: Dict[str, Any],
        context_vectors: Optional[List[List[float]]] = None
    ) -> Dict[str, Any]:
        """
        Przetwarzanie ProjectVector (tylko new orchestrator).
        
        Args:
            project_vector: ProjectVector jako dict
            context_vectors: Wektory kontekstowe
        
        Returns:
            Dict z wynikami
        """
        if self.unified and NEW_AVAILABLE:
            return self.unified.process_projectvector(
                project_vector=project_vector,
                context_vectors=context_vectors,
                adaptive_mode=True
            )
        else:
            return {
                "error": "UnifiedOrchestrator not available",
                "status": "ERROR",
                "fallback": "Use process_intent() with legacy mode"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Status bridge."""
        return {
            "active_mode": self.active_mode,
            "legacy_available": LEGACY_AVAILABLE and self.legacy is not None,
            "new_available": NEW_AVAILABLE and self.new is not None,
            "unified_available": NEW_AVAILABLE and self.unified is not None,
            "architect_id": self.architect_id
        }


# ============================================================================
# PRZYKŁAD UŻYCIA
# ============================================================================

def example_bridge_usage():
    """Przykład użycia bridge."""
    
    # Inicjalizacja bridge (automatycznie wybierze najlepszy tryb)
    bridge = OrchestratorBridge(
        architect_id="PATRYK_SOBIERANSKI_PM",
        prefer_new=True
    )
    
    # Status
    print("\n" + "="*70)
    print("ORCHESTRATOR BRIDGE — STATUS")
    print("="*70)
    status = bridge.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    print("="*70)
    
    # Przykład 1: Podstawowy intent
    print("\n[PRZYKŁAD 1] Podstawowy intent (bez embeddings)")
    result1 = bridge.process_intent(
        intent_text="Optymalizacja T_Causality do 1000 req/s",
        priority=0.9
    )
    print(f"Mode: {result1.get('mode')}")
    print(f"Status: {result1.get('status')}")
    
    # Przykład 2: Intent z embeddings (tylko new orchestrator)
    if bridge.active_mode == "NEW":
        print("\n[PRZYKŁAD 2] Intent z embeddings")
        result2 = bridge.process_intent(
            intent_text="Analiza trendu globalnego AI w edukacji",
            embeddings=[0.1 * i for i in range(128)],
            context_vectors=[
                [0.2 * i for i in range(128)],
                [0.3 * i for i in range(128)]
            ],
            priority=0.8
        )
        print(f"Synthesis Score: {result2.get('synthesis_score', 0):.4f}")
        print(f"Meta Score: {result2.get('meta_score', 0):.4f}")
        print(f"GVS: {result2.get('global_vision_score', 0):.4f}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    example_bridge_usage()
