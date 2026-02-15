"""
ORCHESTRATOR v2.0 — Centralny Mózg GlobalVision Core
======================================================

Punkt wejścia dla całego ekosystemu META-GENIUSZ AGI System.
Integracja: ASQK-7G, ASQK-META, GlobalVision, Inference, T_Causality.

Architektura:
    INPUT: IntentVector (ProjectVector compatible)
    PIPELINE: 7G Synth → META Synth → GlobalVision → Inference → Decision
    OUTPUT: ActionVector + Meta-Score + Recommendations

Wersja: 2.0
Data: 2026-02-03
Autor: Patryk Sobierański (META-GENIUSZ®)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
import logging
import json

# CORE imports
try:
    from CORE.ASQK_7G import asqk_7g_core
    ASQK_7G_AVAILABLE = True
except ImportError:
    ASQK_7G_AVAILABLE = False

try:
    from CORE.ASQK_META import asqk_meta_core
    ASQK_META_AVAILABLE = True
except ImportError:
    ASQK_META_AVAILABLE = False

# Logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class IntentVector:
    """
    Wektor intencji wejściowej (zgodny z ProjectVector).
    """
    intent_id: str
    intent_text: str
    intent_embedding: List[float] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    priority: float = 1.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SynthesisResult:
    """
    Wynik syntezy lokalnej (ASQK-7G).
    """
    status: str
    score: float
    vector: List[float]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class MetaSynthesisResult:
    """
    Wynik meta-syntezy (ASQK-META).
    """
    status: str
    meta_score: float
    meta_vector: List[float]
    aggregation_mode: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class OrchestratorResponse:
    """
    Odpowiedź orkiestratora — finalna decyzja systemu.
    """
    intent_id: str
    status: str
    synthesis_result: Optional[SynthesisResult] = None
    meta_synthesis_result: Optional[MetaSynthesisResult] = None
    global_vision_score: float = 0.0
    action_vector: List[float] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Konwersja do słownika."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Konwersja do JSON."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


# ============================================================================
# ORCHESTRATOR CORE
# ============================================================================

class OrchestratorV2:
    """
    Centralny Orkiestrator v2.0
    
    Funkcje:
        - Przyjmuje IntentVector
        - Wykonuje syntezę lokalną (ASQK-7G)
        - Wykonuje meta-syntezę (ASQK-META)
        - Integruje z GlobalVision
        - Zwraca ActionVector + rekomendacje
    """
    
    def __init__(
        self,
        asqk_7g_enabled: bool = True,
        asqk_meta_enabled: bool = True,
        inference_enabled: bool = True,
        log_level: str = "INFO"
    ):
        """
        Inicjalizacja orkiestratora.
        
        Args:
            asqk_7g_enabled: Włącz syntezę lokalną ASQK-7G
            asqk_meta_enabled: Włącz meta-syntezę ASQK-META
            inference_enabled: Włącz warstwę inferencji (T_Causality)
            log_level: Poziom logowania
        """
        self.asqk_7g_enabled = asqk_7g_enabled and ASQK_7G_AVAILABLE
        self.asqk_meta_enabled = asqk_meta_enabled and ASQK_META_AVAILABLE
        self.inference_enabled = inference_enabled
        
        # Historia cykli
        self.cycle_history: List[OrchestratorResponse] = []
        
        # Konfiguracja logowania
        logger.setLevel(log_level)
        
        # Status inicjalizacji
        logger.info("=" * 70)
        logger.info("ORCHESTRATOR v2.0 — INICJALIZACJA")
        logger.info("=" * 70)
        logger.info(f"ASQK-7G:     {'✓ AKTYWNY' if self.asqk_7g_enabled else '✗ NIEAKTYWNY'}")
        logger.info(f"ASQK-META:   {'✓ AKTYWNY' if self.asqk_meta_enabled else '✗ NIEAKTYWNY'}")
        logger.info(f"Inference:   {'✓ AKTYWNY' if self.inference_enabled else '✗ NIEAKTYWNY'}")
        logger.info("=" * 70)
    
    def process_intent(
        self,
        intent: IntentVector,
        context_vectors: Optional[List[List[float]]] = None,
        adaptive_mode: bool = False
    ) -> OrchestratorResponse:
        """
        Główna funkcja przetwarzania intencji.
        
        Pipeline:
            1. Synteza lokalna (ASQK-7G)
            2. Meta-synteza (ASQK-META) — jeśli context_vectors dostępne
            3. GlobalVision scoring
            4. Inference (T_Causality)
            5. Generacja ActionVector
            6. Rekomendacje
        
        Args:
            intent: Wektor intencji wejściowej
            context_vectors: Lista wektorów kontekstowych (opcjonalne)
            adaptive_mode: Tryb adaptacyjny dla ASQK-7G
        
        Returns:
            OrchestratorResponse z pełnym wynikiem przetwarzania
        """
        start_time = datetime.now()
        logger.info("")
        logger.info("=" * 70)
        logger.info(f"NOWY CYKL ORKIESTRACJI | Intent ID: {intent.intent_id}")
        logger.info("=" * 70)
        
        # === FAZA 1: SYNTEZA LOKALNA (ASQK-7G) ===
        synthesis_result = None
        if self.asqk_7g_enabled and intent.intent_embedding:
            logger.info("[FAZA 1/5] Synteza lokalna (ASQK-7G)...")
            
            result = asqk_7g_core(
                query_vector=intent.intent_embedding,
                adaptive=adaptive_mode
            )
            
            synthesis_result = SynthesisResult(
                status=result["status"],
                score=result["score"],
                vector=intent.intent_embedding
            )
            
            logger.info(f"  → Status: {result['status']}")
            logger.info(f"  → Score: {result['score']:.4f}")
        else:
            logger.info("[FAZA 1/5] ASQK-7G POMINIETE (brak embeddings lub moduł wyłączony)")
        
        # === FAZA 2: META-SYNTEZA (ASQK-META) ===
        meta_synthesis_result = None
        if self.asqk_meta_enabled and context_vectors:
            logger.info("[FAZA 2/5] Meta-synteza (ASQK-META)...")
            
            # Dodaj intent_embedding do context_vectors
            all_vectors = [intent.intent_embedding] + context_vectors if intent.intent_embedding else context_vectors
            
            result = asqk_meta_core(
                vectors=all_vectors,
                mode="energy"
            )
            
            meta_synthesis_result = MetaSynthesisResult(
                status=result["status"],
                meta_score=result["meta_score"],
                meta_vector=result["meta_vector"],
                aggregation_mode="energy"
            )
            
            logger.info(f"  → Status: {result['status']}")
            logger.info(f"  → Meta-Score: {result['meta_score']:.4f}")
            logger.info(f"  → Meta-Vector Dim: {len(result['meta_vector'])}")
        else:
            logger.info("[FAZA 2/5] ASQK-META POMINIETE (brak wektorów kontekstowych lub moduł wyłączony)")
        
        # === FAZA 3: GLOBALVISION SCORING ===
        logger.info("[FAZA 3/5] GlobalVision Scoring...")
        global_vision_score = self._compute_globalvision_score(
            synthesis_result,
            meta_synthesis_result,
            intent
        )
        logger.info(f"  → Global Vision Score: {global_vision_score:.4f}")
        
        # === FAZA 4: INFERENCE (T_CAUSALITY) ===
        logger.info("[FAZA 4/5] Inference Layer (T_Causality)...")
        if self.inference_enabled:
            # Placeholder — integracja z T_Causality
            logger.info("  → T_Causality: STUB (do implementacji)")
        else:
            logger.info("  → Inference POMINIETE")
        
        # === FAZA 5: ACTION VECTOR + REKOMENDACJE ===
        logger.info("[FAZA 5/5] Generacja ActionVector i rekomendacji...")
        action_vector = self._generate_action_vector(
            synthesis_result,
            meta_synthesis_result
        )
        recommendations = self._generate_recommendations(
            global_vision_score,
            synthesis_result,
            meta_synthesis_result
        )
        
        logger.info(f"  → ActionVector Dim: {len(action_vector)}")
        logger.info(f"  → Rekomendacje: {len(recommendations)}")
        
        # === FINALIZACJA ===
        end_time = datetime.now()
        execution_time_ms = (end_time - start_time).total_seconds() * 1000
        
        response = OrchestratorResponse(
            intent_id=intent.intent_id,
            status="SUCCESS",
            synthesis_result=synthesis_result,
            meta_synthesis_result=meta_synthesis_result,
            global_vision_score=global_vision_score,
            action_vector=action_vector,
            recommendations=recommendations,
            execution_time_ms=execution_time_ms
        )
        
        # Zapisz w historii
        self.cycle_history.append(response)
        
        logger.info("=" * 70)
        logger.info(f"CYKL ZAKOŃCZONY | Czas: {execution_time_ms:.2f} ms")
        logger.info("=" * 70)
        logger.info("")
        
        return response
    
    def _compute_globalvision_score(
        self,
        synthesis_result: Optional[SynthesisResult],
        meta_synthesis_result: Optional[MetaSynthesisResult],
        intent: IntentVector
    ) -> float:
        """
        Obliczenie Global Vision Score.
        
        Formuła:
            GVS = 0.3 * synthesis_score + 0.5 * meta_score + 0.2 * priority
        """
        synthesis_score = synthesis_result.score if synthesis_result else 0.0
        meta_score = meta_synthesis_result.meta_score if meta_synthesis_result else 0.0
        priority = intent.priority
        
        # Normalizacja (0-1)
        synthesis_norm = min(synthesis_score / 10.0, 1.0)
        meta_norm = min(meta_score / 10.0, 1.0)
        priority_norm = min(priority, 1.0)
        
        gvs = 0.3 * synthesis_norm + 0.5 * meta_norm + 0.2 * priority_norm
        return gvs
    
    def _generate_action_vector(
        self,
        synthesis_result: Optional[SynthesisResult],
        meta_synthesis_result: Optional[MetaSynthesisResult]
    ) -> List[float]:
        """
        Generacja Action Vector na podstawie wyników syntezy.
        """
        # Jeśli meta-synteza dostępna, użyj meta_vector
        if meta_synthesis_result and meta_synthesis_result.meta_vector:
            return meta_synthesis_result.meta_vector
        
        # Jeśli tylko synteza lokalna, użyj synthesis_vector
        if synthesis_result and synthesis_result.vector:
            return synthesis_result.vector
        
        # Domyślnie: pusty wektor
        return []
    
    def _generate_recommendations(
        self,
        global_vision_score: float,
        synthesis_result: Optional[SynthesisResult],
        meta_synthesis_result: Optional[MetaSynthesisResult]
    ) -> List[str]:
        """
        Generacja rekomendacji na podstawie wyników.
        """
        recommendations = []
        
        # Rekomendacje na podstawie GVS
        if global_vision_score > 0.8:
            recommendations.append("Wysoki potencjał — priorytet realizacji")
        elif global_vision_score > 0.5:
            recommendations.append("Średni potencjał — wymaga dalszej analizy")
        else:
            recommendations.append("Niski potencjał — rozważ modyfikację intencji")
        
        # Rekomendacje na podstawie syntezy lokalnej
        if synthesis_result and synthesis_result.score > 14.0:
            recommendations.append("Synteza lokalna: silny sygnał wektorowy")
        
        # Rekomendacje na podstawie meta-syntezy
        if meta_synthesis_result and meta_synthesis_result.meta_score > 1.0:
            recommendations.append("Meta-synteza: wysoka energia trendu")
        
        return recommendations
    
    def get_cycle_history(self) -> List[Dict]:
        """Zwróć historię cykli orkiestracji."""
        return [cycle.to_dict() for cycle in self.cycle_history]
    
    def reset_history(self):
        """Wyczyść historię cykli."""
        self.cycle_history = []
        logger.info("Historia cykli wyczyszczona")


# ============================================================================
# PRZYKŁAD UŻYCIA
# ============================================================================

def example_usage():
    """Przykład użycia orkiestratora."""
    
    # Inicjalizacja
    orchestrator = OrchestratorV2(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True,
        inference_enabled=True
    )
    
    # Przykładowy intent
    intent = IntentVector(
        intent_id="INTENT-001",
        intent_text="Analiza trendu globalnego dla projektu X",
        intent_embedding=[1.0, 2.0, 3.0, 4.0, 5.0],
        priority=0.9
    )
    
    # Przykładowe wektory kontekstowe
    context_vectors = [
        [0.5, 1.5, 2.5, 3.5, 4.5],
        [1.2, 2.2, 3.2, 4.2, 5.2],
        [0.8, 1.8, 2.8, 3.8, 4.8]
    ]
    
    # Przetwarzanie
    response = orchestrator.process_intent(
        intent=intent,
        context_vectors=context_vectors,
        adaptive_mode=True
    )
    
    # Wyniki
    print("\n" + "=" * 70)
    print("WYNIKI ORKIESTRACJI")
    print("=" * 70)
    print(response.to_json())
    print("=" * 70)


if __name__ == "__main__":
    example_usage()
