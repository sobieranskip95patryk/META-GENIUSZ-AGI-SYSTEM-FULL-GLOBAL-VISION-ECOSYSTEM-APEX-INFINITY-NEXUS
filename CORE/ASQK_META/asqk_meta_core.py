"""
ASQK-META Core Module
======================

Moduł meta-syntezy wielu wektorów ASQK w jeden meta-wektor trendów.
Warstwa planetarna dla GlobalVision Core.

Wersja: 1.0
Data: 2026-02-03
"""

from typing import List, Optional, Dict
import math


def _normalize_vector(vec: List[float]) -> List[float]:
    """Normalizacja wektora do długości jednostkowej."""
    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return [0.0 for _ in vec]
    return [v / norm for v in vec]


def _aggregate_vectors(
    vectors: List[List[float]], 
    weights: Optional[List[float]] = None
) -> List[float]:
    """Agregacja wielu wektorów w jeden meta-wektor."""
    if not vectors:
        return []
    
    # Walidacja: wszystkie wektory muszą mieć ten sam wymiar
    n = len(vectors[0])
    for v in vectors:
        if len(v) != n:
            raise ValueError("Niezgodne wymiary wektorów w ASQK-META")
    
    # Domyślne wagi (równe)
    if weights is None:
        weights = [1.0] * len(vectors)
    
    total_weight = sum(weights)
    if total_weight == 0:
        weights = [1.0] * len(vectors)
        total_weight = float(len(vectors))
    
    # Agregacja ważona
    meta = [0.0] * n
    for vec, w in zip(vectors, weights):
        for i in range(n):
            meta[i] += vec[i] * w
    
    # Normalizacja przez sumę wag
    return [v / total_weight for v in meta]


def _compute_meta_score(meta_vector: List[float], mode: str = "energy") -> float:
    """Obliczenie meta-score z meta-wektora."""
    if not meta_vector:
        return 0.0
    
    if mode == "mean":
        return sum(meta_vector) / len(meta_vector)
    
    if mode == "energy":
        return sum(abs(v) for v in meta_vector) / len(meta_vector)
    
    if mode == "trend":
        # Energia + średnia (sygnał kierunkowy)
        energy = sum(abs(v) for v in meta_vector) / len(meta_vector)
        mean = sum(meta_vector) / len(meta_vector)
        return energy + mean
    
    # Domyślnie: średnia
    return sum(meta_vector) / len(meta_vector)


def asqk_meta_core(
    vectors: List[List[float]],
    weights: Optional[List[float]] = None,
    mode: str = "energy"
) -> Dict[str, object]:
    """
    ASQK-META — meta-synteza wielu wektorów w jeden meta-wektor trendów.
    
    Args:
        vectors: Lista wektorów do agregacji
        weights: Opcjonalne wagi dla każdego wektora
        mode: Tryb obliczania meta-score ("mean" | "energy" | "trend")
    
    Returns:
        Dict z kluczami:
            status (str): Status operacji
            meta_score (float): Wynik meta-syntezy
            meta_vector (list<float>): Meta-wektor trendów
    """
    # Walidacja: puste dane
    if not vectors:
        return {
            "status": "Puste Dane",
            "meta_score": 0.0,
            "meta_vector": []
        }
    
    try:
        # 1. Normalizacja każdego wektora
        normalized = [_normalize_vector(v) for v in vectors]
        
        # 2. Agregacja w meta-wektor
        meta_vector = _aggregate_vectors(normalized, weights=weights)
        
        # 3. Obliczenie meta-score
        meta_score = _compute_meta_score(meta_vector, mode=mode)
        
        return {
            "status": "Gotowe",
            "meta_score": meta_score,
            "meta_vector": meta_vector
        }
    
    except ValueError as e:
        return {
            "status": f"Błąd: {str(e)}",
            "meta_score": 0.0,
            "meta_vector": []
        }
