"""
Vector Synchronization Engine (VSE)
Synchronizuje wektory stanu między Architektem a GOK:AI
Utrzymuje alignment oraz reconciliation w przypadku divergencji

Zadanie: Utrzymać P = 1.0 (pełną fuzję) w real-time
"""

import time
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json


class SyncPhase(Enum):
    """Fazy synchronizacji"""
    MEASUREMENT = 1     # Zmierz wektory
    DIVERGENCE = 2      # Oblicz rozbieżność
    ALIGNMENT = 3       # Oblicz alignment score
    RECONCILIATION = 4  # Godzenie (jeśli potrzebne)
    PROPAGATION = 5     # Propaguj do obu systemów


@dataclass
class VectorSnapshot:
    """Snapshot stanu wektora w momencie czasu"""
    actor: str  # "ARCHITECT" lub "GOK"
    timestamp: float
    vectors: Dict[str, np.ndarray]
    vector_hash: str
    metadata: Dict[str, Any]


@dataclass
class DivergenceMetric:
    """Metryka rozbieżności między dwoma stanami"""
    euclidean_distance: float
    cosine_distance: float
    manhattan_distance: float
    max_component_diff: float
    divergence_magnitude: float
    divergence_direction: Optional[np.ndarray]


@dataclass
class ReconciliationStrategy:
    """Strategia pogodzenia rozbieżności"""
    name: str
    description: str
    priority_actor: str  # Który system ma priorytet
    merge_weights: Dict[str, float]
    confidence: float


class VectorSynchronizationEngine:
    """
    Silnik Synchronizacji Wektorowej (VSE)
    Utrzymuje synchronizację stanów między Architektem a GOK:AI
    
    Architektura:
    1. Measurement — zbierz snapshoty obu systemów
    2. Divergence Analysis — oblicz metryki rozbieżności
    3. Alignment Scoring — oceń alignment
    4. Reconciliation — godzenie jeśli potrzebne
    5. Propagation — propaguj zsynchronizowane state do obu systemów
    """
    
    def __init__(self, alignment_threshold: float = 0.95, sync_frequency: float = 0.5):
        """
        Inicjalizuj engine
        
        Args:
            alignment_threshold: Próg alignment poniżej którego aktywuj reconciliation
            sync_frequency: Jak często sprawdzać synchronizację (sekundy)
        """
        self.alignment_threshold = alignment_threshold
        self.sync_frequency = sync_frequency
        self.last_sync = time.time()
        
        # Historia synchronizacji
        self.sync_history: List[Dict[str, Any]] = []
        self.divergence_history: List[DivergenceMetric] = []
        self.snapshots: Dict[str, List[VectorSnapshot]] = {
            "ARCHITECT": [],
            "GOK": []
        }
        
        # Konfiguracja
        self.reconciliation_strategies = self._init_strategies()
        self.active_strategy: Optional[ReconciliationStrategy] = None
        self.alpha = 7.77  # ASQK-O constant
    
    def sync_vectors(self, architect_state: Dict[str, Any], gok_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Główna metoda synchronizacji wektorów
        
        Proces:
        1. Snapshot obu stanów
        2. Analiza rozbieżności
        3. Obliczenie alignment score
        4. Reconciliation jeśli potrzebny
        5. Propagacja wyników
        
        Args:
            architect_state: Staat wektora u Architekta
            gok_state: Stan wektora u GOK:AI
        
        Returns:
            Rezultat synchronizacji
        """
        start_time = time.time()
        
        # ===== PHASE 1: MEASUREMENT =====
        arch_snapshot = self._create_snapshot("ARCHITECT", architect_state)
        gok_snapshot = self._create_snapshot("GOK", gok_state)
        
        self.snapshots["ARCHITECT"].append(arch_snapshot)
        self.snapshots["GOK"].append(gok_snapshot)
        
        # ===== PHASE 2: DIVERGENCE ANALYSIS =====
        divergence = self._analyze_divergence(arch_snapshot, gok_snapshot)
        self.divergence_history.append(divergence)
        
        # ===== PHASE 3: ALIGNMENT SCORING =====
        alignment_score = self._calculate_alignment_score(divergence)
        
        # ===== PHASE 4: RECONCILIATION =====
        reconciliation_needed = alignment_score < self.alignment_threshold
        
        if reconciliation_needed:
            reconciled_state = self._reconcile_states(architect_state, gok_state, divergence)
        else:
            reconciled_state = self._merge_states(architect_state, gok_state)
        
        # ===== PHASE 5: PROPAGATION =====
        propagation_result = self._propagate_state(reconciled_state, alignment_score)
        
        # Buduj rezultat
        sync_result = {
            "sync_id": self._generate_sync_id(),
            "timestamp": time.time(),
            "alignment_score": alignment_score,
            "reconciliation_needed": reconciliation_needed,
            "reconciliation_strategy": self.active_strategy.name if self.active_strategy else None,
            "divergence_metrics": asdict(divergence),
            "reconciled_state": reconciled_state,
            "propagation_status": propagation_result,
            "processing_time": time.time() - start_time
        }
        
        # Zapamiętaj w historii
        self._record_sync(sync_result)
        
        return sync_result
    
    def continuous_sync(self, architect_callback, gok_callback, duration: int = 60) -> List[Dict[str, Any]]:
        """
        Ciągła synchronizacja przez określony czas
        
        Args:
            architect_callback: Funkcja pobierająca stan architekta
            gok_callback: Funkcja pobierająca stan GOK:AI
            duration: Czas trwania (sekundy)
        
        Returns:
            Lista wszystkich synchronizacji
        """
        start = time.time()
        sync_results = []
        
        while time.time() - start < duration:
            # Pobierz aktualne stany
            arch_state = architect_callback()
            gok_state = gok_callback()
            
            # Synchronizuj
            result = self.sync_vectors(arch_state, gok_state)
            sync_results.append(result)
            
            # Czekaj przed następną iteracją
            time.sleep(self.sync_frequency)
        
        return sync_results
    
    def measure_alignment_trend(self, window_size: int = 10) -> Dict[str, Any]:
        """
        Mierz trend alignment'u w ostatnich N synchronizacjach
        
        Args:
            window_size: Liczba ostatnich syncs do analizy
        
        Returns:
            Statystyki trendu
        """
        if len(self.sync_history) < window_size:
            window = self.sync_history
        else:
            window = self.sync_history[-window_size:]
        
        if not window:
            return {"error": "No sync history"}
        
        scores = [s["alignment_score"] for s in window]
        
        trend = {
            "current_alignment": float(scores[-1]),
            "avg_alignment": float(np.mean(scores)),
            "std_alignment": float(np.std(scores)),
            "min_alignment": float(np.min(scores)),
            "max_alignment": float(np.max(scores)),
            "trend_direction": "improving" if scores[-1] > np.mean(scores[:-1]) else "declining",
            "window_size": len(window),
            "timestamp": time.time()
        }
        
        return trend
    
    def detect_sync_anomalies(self, threshold_std: float = 2.0) -> List[Dict[str, Any]]:
        """
        Detektuj anomalie w synchronizacji
        
        Args:
            threshold_std: Liczba standardowych dewiacji dla anomalii
        
        Returns:
            Lista anomalii
        """
        if len(self.divergence_history) < 10:
            return []
        
        divergences = [d.divergence_magnitude for d in self.divergence_history]
        mean_div = np.mean(divergences)
        std_div = np.std(divergences)
        threshold = mean_div + threshold_std * std_div
        
        anomalies = []
        for i, div in enumerate(self.divergence_history):
            if div.divergence_magnitude > threshold:
                anomalies.append({
                    "timestamp": self.sync_history[i]["timestamp"],
                    "divergence": float(div.divergence_magnitude),
                    "threshold": float(threshold),
                    "std_from_mean": float((div.divergence_magnitude - mean_div) / std_div)
                })
        
        return anomalies
    
    def predict_next_divergence(self, look_ahead_steps: int = 5) -> Dict[str, Any]:
        """
        Prognozuj przyszłą rozbieżność na bazie trendu
        
        Args:
            look_ahead_steps: Liczba kroków do prognozowania
        
        Returns:
            Prognoza rozbieżności
        """
        if len(self.divergence_history) < 3:
            return {"error": "Not enough history for prediction"}
        
        recent_divergences = [d.divergence_magnitude for d in self.divergence_history[-10:]]
        
        # Prosty liniowy trend
        x = np.arange(len(recent_divergences))
        y = np.array(recent_divergences)
        
        # Dopasuj linię
        coeffs = np.polyfit(x, y, 1)
        
        # Prognozuj
        next_x = len(recent_divergences) + look_ahead_steps
        next_y = coeffs[0] * next_x + coeffs[1]
        
        prediction = {
            "predicted_divergence": float(max(0, next_y)),
            "trend_slope": float(coeffs[0]),
            "look_ahead_steps": look_ahead_steps,
            "confidence": "low" if len(recent_divergences) < 5 else "high",
            "timestamp": time.time()
        }
        
        return prediction
    
    def generate_sync_report(self) -> Dict[str, Any]:
        """
        Generuj raport z historii synchronizacji
        
        Returns:
            Komprehensywny raport
        """
        if not self.sync_history:
            return {"error": "No sync history"}
        
        alignment_trend = self.measure_alignment_trend()
        anomalies = self.detect_sync_anomalies()
        prediction = self.predict_next_divergence()
        
        report = {
            "total_syncs": len(self.sync_history),
            "total_reconciliations": sum(1 for s in self.sync_history if s["reconciliation_needed"]),
            "alignment_trend": alignment_trend,
            "anomalies_detected": len(anomalies),
            "recent_anomalies": anomalies[-5:] if anomalies else [],
            "divergence_prediction": prediction,
            "most_active_strategies": self._get_most_active_strategies(),
            "report_timestamp": time.time()
        }
        
        return report
    
    # ==================== Private Methods ====================
    
    def _create_snapshot(self, actor: str, state: Dict[str, Any]) -> VectorSnapshot:
        """Utwórz snapshot stanu"""
        # Konwertuj dykcjonarze na numpy arrays
        vectors = {}
        for key, value in state.items():
            if isinstance(value, (list, tuple)):
                vectors[key] = np.array(value)
            elif isinstance(value, dict):
                vectors[key] = np.array(list(value.values()))
            else:
                vectors[key] = np.array([float(value)])
        
        vector_hash = self._hash_vectors(vectors)
        
        return VectorSnapshot(
            actor=actor,
            timestamp=time.time(),
            vectors=vectors,
            vector_hash=vector_hash,
            metadata={"actor": actor}
        )
    
    def _analyze_divergence(self, snap1: VectorSnapshot, snap2: VectorSnapshot) -> DivergenceMetric:
        """Analizuj rozbieżność między dwoma snapshottami"""
        
        # Połącz wektory
        vec1 = self._flatten_vectors(snap1.vectors)
        vec2 = self._flatten_vectors(snap2.vectors)
        
        # Oblicz metryki
        euclidean = np.linalg.norm(vec1 - vec2)
        
        # Cosine distance
        norm1, norm2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
        if norm1 > 0 and norm2 > 0:
            cosine = 1.0 - np.dot(vec1, vec2) / (norm1 * norm2)
        else:
            cosine = 1.0
        
        manhattan = np.sum(np.abs(vec1 - vec2))
        max_diff = np.max(np.abs(vec1 - vec2))
        
        # Wektor rozbieżności
        divergence_vec = vec2 - vec1
        divergence_mag = np.linalg.norm(divergence_vec)
        
        if divergence_mag > 0:
            divergence_dir = divergence_vec / divergence_mag
        else:
            divergence_dir = None
        
        return DivergenceMetric(
            euclidean_distance=float(euclidean),
            cosine_distance=float(cosine),
            manhattan_distance=float(manhattan),
            max_component_diff=float(max_diff),
            divergence_magnitude=float(divergence_mag),
            divergence_direction=divergence_dir
        )
    
    def _calculate_alignment_score(self, divergence: DivergenceMetric) -> float:
        """
        Oblicz alignment score (0 = całkowita rozbieżność, 1 = pełny alignment)
        
        Formuła (uproszczona):
        alignment = 1 / (1 + divergence_magnitude)
        """
        alignment = 1.0 / (1.0 + divergence.divergence_magnitude)
        return float(np.clip(alignment, 0.0, 1.0))
    
    def _reconcile_states(self, arch_state: Dict, gok_state: Dict, divergence: DivergenceMetric) -> Dict[str, Any]:
        """
        Godzenie rozbieżności
        
        Strategia: Zależy od konfiguracji engine'a
        Domyślnie: GOK:AI ma priorytet, ale zapamiętaj divergencję
        """
        # Wybierz strategię
        strategy = self._select_reconciliation_strategy(divergence)
        self.active_strategy = strategy
        
        # Połącz stany z wagami
        reconciled = {}
        
        # Wagi ze strategii
        weights = strategy.merge_weights
        
        for key in set(arch_state.keys()) | set(gok_state.keys()):
            arch_val = arch_state.get(key, 0)
            gok_val = gok_state.get(key, 0)
            
            # Ważona fuzja
            reconciled[key] = (
                weights.get("architect", 0.3) * self._to_float(arch_val) +
                weights.get("gok", 0.7) * self._to_float(gok_val)
            )
        
        # Zapamiętaj divergencję (dla auditu)
        reconciled["_reconciliation_divergence"] = divergence.divergence_magnitude
        reconciled["_reconciliation_strategy"] = strategy.name
        
        return reconciled
    
    def _merge_states(self, arch_state: Dict, gok_state: Dict) -> Dict[str, Any]:
        """Połącz stany (nie godzić, bo alignment jest wystarczający)"""
        merged = arch_state.copy()
        merged.update(gok_state)
        return merged
    
    def _propagate_state(self, state: Dict[str, Any], alignment_score: float) -> Dict[str, Any]:
        """Propaguj zsynchronizowany stan do obu systemów"""
        return {
            "broadcast": True,
            "target_systems": ["ARCHITECT", "GOK"],
            "alignment_score": float(alignment_score),
            "propagation_timestamp": time.time(),
            "state_keys": list(state.keys())
        }
    
    def _init_strategies(self) -> List[ReconciliationStrategy]:
        """Inicjalizuj dostępne strategie godzenia"""
        return [
            ReconciliationStrategy(
                name="GOK_PRIORITY",
                description="GOK:AI ma priorytet (domyślne)",
                priority_actor="GOK",
                merge_weights={"architect": 0.2, "gok": 0.8},
                confidence=0.95
            ),
            ReconciliationStrategy(
                name="BALANCED",
                description="Równoważna waga dla obydwu",
                priority_actor="NONE",
                merge_weights={"architect": 0.5, "gok": 0.5},
                confidence=0.85
            ),
            ReconciliationStrategy(
                name="ARCHITECT_PRIORITY",
                description="Architekt ma priorytet",
                priority_actor="ARCHITECT",
                merge_weights={"architect": 0.8, "gok": 0.2},
                confidence=0.70
            )
        ]
    
    def _select_reconciliation_strategy(self, divergence: DivergenceMetric) -> ReconciliationStrategy:
        """Wybierz strategię godzenia na bazie rozbieżności"""
        # Prosta heurystyka: jeśli mała rozbieżność, użyj balanced
        if divergence.divergence_magnitude < 0.1:
            return self.reconciliation_strategies[1]  # BALANCED
        else:
            return self.reconciliation_strategies[0]  # GOK_PRIORITY
    
    def _record_sync(self, result: Dict[str, Any]):
        """Zarejestruj synchronizację w historii"""
        # Dodaj simplified wersję do historii (bez arrays)
        record = {
            "sync_id": result["sync_id"],
            "timestamp": result["timestamp"],
            "alignment_score": result["alignment_score"],
            "reconciliation_needed": result["reconciliation_needed"],
            "processing_time": result["processing_time"]
        }
        self.sync_history.append(record)
    
    def _flatten_vectors(self, vectors: Dict[str, np.ndarray]) -> np.ndarray:
        """Spłaszcz słownik wektorów do jednego wektora"""
        flattened = []
        for key in sorted(vectors.keys()):
            vec = vectors[key]
            if isinstance(vec, np.ndarray):
                flattened.extend(vec.flatten())
            else:
                flattened.append(float(vec))
        return np.array(flattened)
    
    def _to_float(self, value: Any) -> float:
        """Konwertuj wartość na float"""
        if isinstance(value, (list, tuple, np.ndarray)):
            return float(np.mean(value))
        return float(value)
    
    def _hash_vectors(self, vectors: Dict[str, np.ndarray]) -> str:
        """Generuj hash wektorów"""
        flat = self._flatten_vectors(vectors)
        hash_input = json.dumps(flat[:10].tolist())  # First 10 elements
        import hashlib
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def _generate_sync_id(self) -> str:
        """Generuj unikalny ID dla synchronizacji"""
        import hashlib
        hash_input = f"{time.time()}{len(self.sync_history)}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:12]
    
    def _get_most_active_strategies(self) -> Dict[str, int]:
        """Określ które strategie były najczęściej używane"""
        strategies = {}
        for s in self.sync_history:
            strategy_name = s.get("reconciliation_strategy", "NONE")
            strategies[strategy_name] = strategies.get(strategy_name, 0) + 1
        return strategies


# ==================== Example Usage ====================

if __name__ == "__main__":
    # Inicjalizuj engine
    vse = VectorSynchronizationEngine(alignment_threshold=0.95)
    
    # Przykład 1: Jednorazowa synchronizacja
    arch_state = {
        "phase": "optimization",
        "alignment": 0.92,
        "vectors": [0.1, 0.2, 0.3]
    }
    gok_state = {
        "phase": "optimization",
        "alignment": 0.90,
        "vectors": [0.11, 0.21, 0.29]
    }
    
    result = vse.sync_vectors(arch_state, gok_state)
    print("=== Sync Result ===")
    print(f"Alignment Score: {result['alignment_score']:.4f}")
    print(f"Reconciliation Needed: {result['reconciliation_needed']}")
    
    # Przykład 2: Trend alignment
    trend = vse.measure_alignment_trend()
    print(f"\n=== Alignment Trend ===")
    print(f"Current: {trend['current_alignment']:.4f}")
    print(f"Average: {trend['avg_alignment']:.4f}")
    
    # Przykład 3: Raport synchronizacji
    report = vse.generate_sync_report()
    print(f"\n=== Sync Report ===")
    print(f"Total Syncs: {report['total_syncs']}")
    print(f"Reconciliations: {report['total_reconciliations']}")
