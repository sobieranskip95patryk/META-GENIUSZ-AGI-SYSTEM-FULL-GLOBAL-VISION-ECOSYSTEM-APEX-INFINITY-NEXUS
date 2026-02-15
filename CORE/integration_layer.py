"""
ORCHESTRATOR Integration Layer
================================

Warstwa integracyjna łącząca:
- ASQK-7G (synteza lokalna)
- ASQK-META (meta-synteza)
- GlobalVision (scoring)
- Inference (T_Causality)
- ProjectVector (standard danych)

Wersja: 1.0
Data: 2026-02-03
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import logging

try:
    from CORE.orchestrator_v2 import OrchestratorV2, IntentVector, OrchestratorResponse
    ORCHESTRATOR_AVAILABLE = True
except ImportError:
    ORCHESTRATOR_AVAILABLE = False

logger = logging.getLogger(__name__)


# ============================================================================
# INTEGRATION ADAPTERS
# ============================================================================

class GlobalVisionAdapter:
    """
    Adapter dla integracji z GlobalVision Core.
    """
    
    def __init__(self):
        self.initialized = False
        logger.info("[GlobalVisionAdapter] Inicjalizacja...")
    
    def compute_gis_score(
        self,
        project_vector: Dict[str, Any],
        synthesis_result: Any
    ) -> float:
        """
        Obliczenie Global Impact Score (GIS).
        
        Args:
            project_vector: ProjectVector jako dict
            synthesis_result: Wynik syntezy ASQK
        
        Returns:
            GIS score (0-10000)
        """
        # Placeholder — integracja z rzeczywistym GlobalVision
        base_score = synthesis_result.score if hasattr(synthesis_result, 'score') else 0.0
        priority = project_vector.get('priority', 1.0)
        
        gis = base_score * priority * 100
        return min(gis, 10000.0)
    
    def compute_pri_score(
        self,
        project_vector: Dict[str, Any],
        meta_result: Any
    ) -> float:
        """
        Obliczenie Planetary Resonance Index (PRI).
        
        Args:
            project_vector: ProjectVector jako dict
            meta_result: Wynik meta-syntezy ASQK-META
        
        Returns:
            PRI score (0-1)
        """
        # Placeholder
        if hasattr(meta_result, 'meta_score'):
            return min(meta_result.meta_score / 10.0, 1.0)
        return 0.0


class InferenceAdapter:
    """
    Adapter dla integracji z warstwą Inference (T_Causality).
    """
    
    def __init__(self):
        self.initialized = False
        logger.info("[InferenceAdapter] Inicjalizacja...")
    
    def compute_causal_pathway(
        self,
        intent_vector: Any,
        action_vector: List[float]
    ) -> Dict[str, Any]:
        """
        Obliczenie ścieżki przyczynowej (T_Causality).
        
        Args:
            intent_vector: Wektor intencji
            action_vector: Wektor akcji
        
        Returns:
            Dict z informacjami o ścieżce przyczynowej
        """
        # Placeholder — integracja z T_Causality
        return {
            "pathway_valid": True,
            "causality_strength": 0.85,
            "intervention_needed": False
        }


class ProjectVectorAdapter:
    """
    Adapter dla konwersji między IntentVector a ProjectVector.
    """
    
    @staticmethod
    def intent_to_projectvector(intent: IntentVector) -> Dict[str, Any]:
        """
        Konwersja IntentVector → ProjectVector.
        
        Args:
            intent: IntentVector z orkiestratora
        
        Returns:
            ProjectVector jako dict
        """
        return {
            "ProjectVector": {
                "id": intent.intent_id,
                "name": intent.intent_text,
                "timestamp": intent.timestamp,
                "priority": intent.priority,
                "intent_embedding": intent.intent_embedding,
                "context": intent.context
            }
        }
    
    @staticmethod
    def projectvector_to_intent(pv: Dict[str, Any]) -> IntentVector:
        """
        Konwersja ProjectVector → IntentVector.
        
        Args:
            pv: ProjectVector jako dict
        
        Returns:
            IntentVector dla orkiestratora
        """
        pv_data = pv.get("ProjectVector", pv)
        
        return IntentVector(
            intent_id=pv_data.get("id", "UNKNOWN"),
            intent_text=pv_data.get("name", ""),
            intent_embedding=pv_data.get("intent_embedding", []),
            context=pv_data.get("context", {}),
            priority=pv_data.get("priority", 1.0),
            timestamp=pv_data.get("timestamp", "")
        )


# ============================================================================
# UNIFIED ORCHESTRATOR INTERFACE
# ============================================================================

class UnifiedOrchestrator:
    """
    Zunifikowany interfejs orkiestratora z pełną integracją.
    
    Integruje:
        - OrchestratorV2 (core)
        - GlobalVisionAdapter
        - InferenceAdapter
        - ProjectVectorAdapter
    """
    
    def __init__(
        self,
        asqk_7g_enabled: bool = True,
        asqk_meta_enabled: bool = True,
        globalvision_enabled: bool = True,
        inference_enabled: bool = True
    ):
        """
        Inicjalizacja zunifikowanego orkiestratora.
        """
        # Core orchestrator
        if ORCHESTRATOR_AVAILABLE:
            self.core = OrchestratorV2(
                asqk_7g_enabled=asqk_7g_enabled,
                asqk_meta_enabled=asqk_meta_enabled,
                inference_enabled=inference_enabled
            )
        else:
            raise ImportError("OrchestratorV2 niedostępny — sprawdź CORE.orchestrator_v2")
        
        # Adaptery
        self.globalvision = GlobalVisionAdapter() if globalvision_enabled else None
        self.inference = InferenceAdapter() if inference_enabled else None
        self.pv_adapter = ProjectVectorAdapter()
        
        logger.info("[UnifiedOrchestrator] Inicjalizacja zakończona")
    
    def process_projectvector(
        self,
        project_vector: Dict[str, Any],
        context_vectors: Optional[List[List[float]]] = None,
        adaptive_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Przetwarzanie ProjectVector przez pełny pipeline.
        
        Args:
            project_vector: ProjectVector jako dict
            context_vectors: Lista wektorów kontekstowych
            adaptive_mode: Tryb adaptacyjny
        
        Returns:
            Dict z pełnymi wynikami (kompatybilny z ProjectVector)
        """
        # Konwersja ProjectVector → IntentVector
        intent = self.pv_adapter.projectvector_to_intent(project_vector)
        
        # Przetwarzanie przez core orchestrator
        response = self.core.process_intent(
            intent=intent,
            context_vectors=context_vectors,
            adaptive_mode=adaptive_mode
        )
        
        # Wzbogacenie o GlobalVision
        if self.globalvision and response.synthesis_result:
            gis_score = self.globalvision.compute_gis_score(
                project_vector,
                response.synthesis_result
            )
            pri_score = self.globalvision.compute_pri_score(
                project_vector,
                response.meta_synthesis_result
            )
            
            response.global_vision_score = gis_score
        
        # Wzbogacenie o Inference
        if self.inference and response.action_vector:
            causal_info = self.inference.compute_causal_pathway(
                intent,
                response.action_vector
            )
            response.recommendations.append(
                f"T_Causality: {causal_info['causality_strength']:.2f}"
            )
        
        # Zwróć jako dict
        return response.to_dict()
    
    def batch_process(
        self,
        project_vectors: List[Dict[str, Any]],
        adaptive_mode: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Przetwarzanie wsadowe wielu ProjectVectors.
        
        Args:
            project_vectors: Lista ProjectVectors
            adaptive_mode: Tryb adaptacyjny
        
        Returns:
            Lista wyników przetwarzania
        """
        results = []
        for pv in project_vectors:
            try:
                result = self.process_projectvector(pv, adaptive_mode=adaptive_mode)
                results.append(result)
            except Exception as e:
                logger.error(f"Błąd przetwarzania ProjectVector {pv.get('id', 'UNKNOWN')}: {e}")
                results.append({
                    "error": str(e),
                    "project_id": pv.get("id", "UNKNOWN")
                })
        
        return results


# ============================================================================
# PRZYKŁAD UŻYCIA
# ============================================================================

def example_integration():
    """Przykład użycia integration layer."""
    
    # Inicjalizacja zunifikowanego orkiestratora
    orchestrator = UnifiedOrchestrator(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True,
        globalvision_enabled=True,
        inference_enabled=True
    )
    
    # Przykładowy ProjectVector
    project_vector = {
        "ProjectVector": {
            "id": "PV-EXAMPLE-001",
            "name": "Analiza trendu AI dla edukacji",
            "priority": 0.9,
            "intent_embedding": [1.0, 2.0, 3.0, 4.0, 5.0],
            "context": {
                "domain": "education",
                "region": "global"
            }
        }
    }
    
    # Przetwarzanie
    result = orchestrator.process_projectvector(
        project_vector=project_vector,
        adaptive_mode=True
    )
    
    # Wyniki
    print("\n" + "=" * 70)
    print("WYNIKI INTEGRACJI")
    print("=" * 70)
    print(f"Intent ID: {result['intent_id']}")
    print(f"Status: {result['status']}")
    print(f"Global Vision Score: {result['global_vision_score']:.4f}")
    print(f"Rekomendacje: {result['recommendations']}")
    print("=" * 70)


if __name__ == "__main__":
    example_integration()
