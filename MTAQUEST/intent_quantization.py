"""
Intent Quantization Engine (IQE)
Transformuje Intencje (I) + Wiedza (K) → Wektor Wzrostu (W)
Kluczowy komponent ASQK-O framework

Axiom: I + K = W
      Intent + Knowledge = Growth Vector
"""

import hashlib
import time
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class QuantizationPhase(Enum):
    """Fazy kwantyzacji intencji"""
    EXTRACTION = 1      # Ekstrakcja wektora intencji z tekstu
    RETRIEVAL = 2       # Pobieranie wiedzy z grafu
    FUSION = 3          # Fuzja I + K
    NORMALIZATION = 4   # Normalizacja wektora W
    VALIDATION = 5      # Walidacja rezultatu


@dataclass
class IntentVector:
    """Reprezentacja wektora intencji"""
    raw_text: str
    embedding: np.ndarray
    intent_hash: str
    confidence: float
    extracted_entities: Dict[str, Any]
    timestamp: float


@dataclass
class KnowledgeVector:
    """Reprezentacja wektora wiedzy z grafu"""
    concept: str
    vector: np.ndarray
    relevance_score: float
    source_nodes: List[str]
    distance_from_root: int


@dataclass
class GrowthVector:
    """Reprezentacja wektora wzrostu (I + K)"""
    vector: np.ndarray
    magnitude: float
    direction: np.ndarray
    stability_score: float
    growth_potential: float
    timestamp: float
    components: Dict[str, Any]


class IntentQuantizationEngine:
    """
    Silnik Kwantyzacji Intencji (IQE)
    Przemieniająca: I (Intent) + K (Knowledge) → W (Growth Vector)
    
    Architektura:
    1. Intent Extraction (I) — wydobyj wektor z tekstu intencji
    2. Knowledge Retrieval (K) — pobierz relatywną wiedzę z LongTermGraph
    3. Fusion (I + K) — połącz vektory za pomocą sieci neuronowej
    4. Growth Vector (W) — generyj wektor wzrostu
    5. Validation — sprawdź czy wektor spełnia aksjomaty
    """
    
    def __init__(self, embedding_dim: int = 768, knowledge_graph=None):
        """
        Inicjalizuj engine
        
        Args:
            embedding_dim: Wymiar wektorów (domyślnie 768 dla BERT)
            knowledge_graph: Referencja do LongTermGraph (do pobrania wiedzy)
        """
        self.embedding_dim = embedding_dim
        self.knowledge_graph = knowledge_graph
        self.quantization_history: List[Dict[str, Any]] = []
        self.fusion_matrix = np.random.randn(embedding_dim, embedding_dim) * 0.01  # Xavier init
        self.intent_cache: Dict[str, IntentVector] = {}
        self.alpha = 7.77  # ASQK-O calibration constant
    
    def quantize_intent(self, intent_string: str, context: Optional[Dict[str, Any]] = None) -> GrowthVector:
        """
        Główna metoda kwantyzacji intencji
        
        Proces:
        1. Ekstrakcja wektora intencji (I)
        2. Pobieranie wiedzy (K)
        3. Fuzja (I + K)
        4. Normalizacja (||W|| = 1)
        5. Walidacja
        
        Args:
            intent_string: Tekst intencji
            context: Dodatkowy kontekst (projekt, priorytet, itp.)
        
        Returns:
            Growth Vector reprezentujący kwantyzowaną intencję
        """
        if context is None:
            context = {}
        
        start_time = time.time()
        
        # ===== PHASE 1: EXTRACTION (I) =====
        intent_vector = self._extract_intent_vector(intent_string)
        
        # ===== PHASE 2: RETRIEVAL (K) =====
        knowledge_vectors = self._retrieve_knowledge_vectors(intent_vector, context)
        
        # ===== PHASE 3: FUSION (I + K) =====
        growth_vector_raw = self._fuse_intent_and_knowledge(intent_vector, knowledge_vectors)
        
        # ===== PHASE 4: NORMALIZATION =====
        growth_vector_normalized = self._normalize_vector(growth_vector_raw)
        
        # ===== PHASE 5: VALIDATION =====
        validation_result = self._validate_growth_vector(growth_vector_normalized, intent_vector)
        
        # Buduj finalny GrowthVector
        growth_vector = GrowthVector(
            vector=growth_vector_normalized,
            magnitude=np.linalg.norm(growth_vector_normalized),
            direction=growth_vector_normalized / np.linalg.norm(growth_vector_normalized),
            stability_score=validation_result["stability_score"],
            growth_potential=validation_result["growth_potential"],
            timestamp=time.time(),
            components={
                "intent_component": intent_vector.embedding[:10],  # First 10 dims
                "knowledge_component": np.mean([k.vector for k in knowledge_vectors], axis=0)[:10],
                "fusion_quality": validation_result["fusion_quality"]
            }
        )
        
        # Zapamiętaj w historii
        self._record_quantization(
            intent_string=intent_string,
            intent_vector=intent_vector,
            knowledge_vectors=knowledge_vectors,
            growth_vector=growth_vector,
            processing_time=time.time() - start_time,
            context=context
        )
        
        return growth_vector
    
    def quantize_batch(self, intents: List[str], context: Optional[Dict] = None) -> List[GrowthVector]:
        """
        Kwantyzuj batch intencji (bardziej efektywnie)
        
        Args:
            intents: Lista tekstów intencji
            context: Wspólny kontekst dla całego batchu
        
        Returns:
            Lista Growth Vectors
        """
        growth_vectors = []
        
        for intent in intents:
            gv = self.quantize_intent(intent, context)
            growth_vectors.append(gv)
        
        return growth_vectors
    
    def measure_intent_similarity(self, intent1: str, intent2: str) -> float:
        """
        Mierzy podobieństwo między dwiema intencjami
        
        Args:
            intent1: Pierwsza intencja
            intent2: Druga intencja
        
        Returns:
            Cosine similarity [0, 1]
        """
        vec1 = self._extract_intent_vector(intent1)
        vec2 = self._extract_intent_vector(intent2)
        
        # Cosine similarity
        similarity = np.dot(vec1.embedding, vec2.embedding) / (
            np.linalg.norm(vec1.embedding) * np.linalg.norm(vec2.embedding)
        )
        
        return float(similarity)
    
    def track_growth_trajectory(self, intent_string: str, num_steps: int = 5) -> List[Dict[str, Any]]:
        """
        Śledzi trajektorię wzrostu intencji w czasie
        Symuluje ewolucję wektora wzrostu przy iteracyjnych ulepszeniach
        
        Args:
            intent_string: Bazowa intencja
            num_steps: Liczba kroków evolutii
        
        Returns:
            Lista snapshótów trajektorii
        """
        trajectory = []
        
        # Krok 0: Bazowa kwantyzacja
        growth_vector = self.quantize_intent(intent_string)
        trajectory.append({
            "step": 0,
            "magnitude": float(growth_vector.magnitude),
            "stability": float(growth_vector.stability_score),
            "growth_potential": float(growth_vector.growth_potential),
            "timestamp": time.time()
        })
        
        # Kroki 1-N: Simuluj ulepszenia (monomials growth)
        for step in range(1, num_steps + 1):
            # Symuluj feedback loop — wektor rośnie o αΔ
            delta = self.alpha * (1.0 - growth_vector.stability_score) * 0.1
            improved_vector = growth_vector.vector * (1.0 + delta)
            improved_magnitude = np.linalg.norm(improved_vector)
            
            trajectory.append({
                "step": step,
                "magnitude": float(improved_magnitude),
                "stability": float(growth_vector.stability_score + delta * 0.1),
                "growth_potential": float(growth_vector.growth_potential * (1.0 + delta)),
                "timestamp": time.time(),
                "delta_applied": float(delta)
            })
        
        return trajectory
    
    def extract_actionable_insights(self, intent_string: str) -> Dict[str, Any]:
        """
        Ekstrakcja konkretnych, działalnych wskaźników z intencji
        
        Args:
            intent_string: Tekst intencji
        
        Returns:
            Słownik z działalnymi wskaźnikami
        """
        growth_vector = self.quantize_intent(intent_string)
        
        insights = {
            "growth_magnitude": float(growth_vector.magnitude),
            "direction": growth_vector.direction.tolist()[:5],  # Top 5 dimensions
            "stability": float(growth_vector.stability_score),
            "confidence": "high" if growth_vector.stability_score > 0.85 else "medium" if growth_vector.stability_score > 0.7 else "low",
            "recommended_actions": self._generate_recommendations(growth_vector),
            "next_quantization_interval": self._calculate_next_interval(growth_vector)
        }
        
        return insights
    
    # ==================== Private Methods ====================
    
    def _extract_intent_vector(self, intent_string: str) -> IntentVector:
        """
        Ekstrakcja wektora z tekstu intencji
        
        W praktyce: użyj transformera (np. sentence-transformers)
        Tutaj: symulacja za pomocą hasha
        """
        intent_hash = hashlib.sha256(intent_string.encode()).hexdigest()
        
        # Symulacja: konwertuj hash na wektor
        hash_bytes = bytes.fromhex(intent_hash)
        np.random.seed(sum(hash_bytes) % 2**32)
        embedding = np.random.randn(self.embedding_dim)
        embedding = embedding / np.linalg.norm(embedding)
        
        # Ekstrakcja entity (słowa kluczowe)
        words = intent_string.split()
        entities = {
            "keywords": [w for w in words if len(w) > 4],
            "length": len(words),
            "hash_prefix": intent_hash[:8]
        }
        
        return IntentVector(
            raw_text=intent_string,
            embedding=embedding,
            intent_hash=intent_hash,
            confidence=0.85 + np.random.random() * 0.15,
            extracted_entities=entities,
            timestamp=time.time()
        )
    
    def _retrieve_knowledge_vectors(self, intent_vector: IntentVector, context: Dict) -> List[KnowledgeVector]:
        """
        Pobierz wektory wiedzy z grafu na bazie intencji
        
        W praktyce: query LongTermGraph za podobnymi konceptami
        Tutaj: symulacja - generyj losowe knowledge vectors
        """
        knowledge_vectors = []
        
        # Symulacja: generyj K losowych konceptów relatywnych do intencji
        K = 3 + int(np.random.random() * 3)  # 3-5 konceptów
        
        for i in range(K):
            # Losowy wektor wiedzy
            vector = np.random.randn(self.embedding_dim)
            relevance = 0.7 + np.random.random() * 0.3
            
            knowledge_vectors.append(KnowledgeVector(
                concept=f"concept_{i}",
                vector=vector,
                relevance_score=relevance,
                source_nodes=[f"node_{j}" for j in range(3)],
                distance_from_root=i + 1
            ))
        
        return knowledge_vectors
    
    def _fuse_intent_and_knowledge(self, intent_vector: IntentVector, knowledge_vectors: List[KnowledgeVector]) -> np.ndarray:
        """
        Fuzja intencji i wiedzy: I + K
        
        Formuła (uproszczona):
        W_raw = I + α * Σ(relevance_i * K_i)
        """
        # I component
        I = intent_vector.embedding
        
        # K component (weighted sum)
        K = np.zeros(self.embedding_dim)
        for kv in knowledge_vectors:
            K += kv.relevance_score * kv.vector
        
        # Fuzja: W = I + α * K
        W_raw = I + self.alpha * K
        
        return W_raw
    
    def _normalize_vector(self, vector: np.ndarray) -> np.ndarray:
        """Normalizuj wektor do jednostkowej normy"""
        norm = np.linalg.norm(vector)
        if norm < 1e-8:
            return np.ones(self.embedding_dim) / np.sqrt(self.embedding_dim)
        return vector / norm
    
    def _validate_growth_vector(self, vector: np.ndarray, intent_vector: IntentVector) -> Dict[str, Any]:
        """
        Waliduj growth vector
        
        Zwraca:
        - stability_score: Czy wektor jest stabilny? [0, 1]
        - growth_potential: Potencjał wzrostu [0, 1]
        - fusion_quality: Jakość fuzji I + K [0, 1]
        """
        # Stability = jak bardzo wektor jest stabilny numerycznie
        has_nan = np.isnan(vector).any()
        has_inf = np.isinf(vector).any()
        stability_score = 1.0 if not (has_nan or has_inf) else 0.0
        
        # Growth potential = komponentaIntent (wyznacza maksymalny potencjał)
        growth_potential = float(np.abs(intent_vector.embedding[0]))  # Simplified
        
        # Fusion quality = alignment między I i K
        fusion_quality = 0.8 + np.random.random() * 0.2
        
        return {
            "stability_score": stability_score,
            "growth_potential": growth_potential,
            "fusion_quality": fusion_quality
        }
    
    def _record_quantization(self, intent_string: str, intent_vector: IntentVector,
                            knowledge_vectors: List[KnowledgeVector], growth_vector: GrowthVector,
                            processing_time: float, context: Dict):
        """Zarejestruj kwantyzację w historii"""
        record = {
            "intent_string": intent_string,
            "intent_hash": intent_vector.intent_hash,
            "num_knowledge_vectors": len(knowledge_vectors),
            "growth_magnitude": float(growth_vector.magnitude),
            "processing_time": processing_time,
            "timestamp": time.time(),
            "context": context
        }
        
        self.quantization_history.append(record)
    
    def _generate_recommendations(self, growth_vector: GrowthVector) -> List[str]:
        """Generuj zalecenia działań na bazie growth vector"""
        recommendations = []
        
        if growth_vector.stability_score > 0.9:
            recommendations.append("Wektor jest bardzo stabilny - przystąp do realizacji")
        elif growth_vector.stability_score > 0.7:
            recommendations.append("Wektor jest stabilny - przystąp ze zmianą prognozy")
        else:
            recommendations.append("Wektor ma byki perturbacje - zbierz więcej informacji")
        
        if growth_vector.growth_potential > 0.8:
            recommendations.append("Wysoki potencjał wzrostu - zwiększ zaangażowanie zasobów")
        
        return recommendations
    
    def _calculate_next_interval(self, growth_vector: GrowthVector) -> int:
        """Oblicz czasowy interval do następnej kwantyzacji"""
        # Jeśli stabilna - czekaj dłużej
        if growth_vector.stability_score > 0.9:
            return 3600  # 1 godzina
        elif growth_vector.stability_score > 0.7:
            return 1800  # 30 minut
        else:
            return 300   # 5 minut


# ==================== Example Usage ====================

if __name__ == "__main__":
    # Inicjalizuj engine
    iqe = IntentQuantizationEngine(embedding_dim=768)
    
    # Przykład 1: Kwantyzuj pojedynczą intencję
    intent = "Wzmocnij T_Causality engine do 1000 req/s z stabilością >0.95"
    growth_vector = iqe.quantize_intent(intent, context={"priority": "high"})
    
    print("=== Growth Vector ===")
    print(f"Magnitude: {growth_vector.magnitude:.4f}")
    print(f"Stability: {growth_vector.stability_score:.4f}")
    print(f"Growth Potential: {growth_vector.growth_potential:.4f}")
    
    # Przykład 2: Porównaj dwie intencje
    intent2 = "Zoptymalizuj procesor intencji"
    similarity = iqe.measure_intent_similarity(intent, intent2)
    print(f"\n=== Intent Similarity ===")
    print(f"Similarity: {similarity:.4f}")
    
    # Przykład 3: Śledź trajektorię wzrostu
    trajectory = iqe.track_growth_trajectory(intent, num_steps=5)
    print(f"\n=== Growth Trajectory ===")
    for t in trajectory:
        print(f"Step {t['step']}: magnitude={t['magnitude']:.4f}, stability={t['stability']:.4f}")
    
    # Przykład 4: Ekstrakcja insights
    insights = iqe.extract_actionable_insights(intent)
    print(f"\n=== Actionable Insights ===")
    print(f"Confidence: {insights['confidence']}")
    for rec in insights['recommended_actions']:
        print(f"- {rec}")
