"""
ASQK-7G Core Module
====================

Moduł syntezy wektorowej z wagami, biasem i trybem adaptacyjnym.
Zgodny z ProjectVector Architecture.

Wersja: 2.0
Data: 2026-02-03
"""

from typing import List, Optional, Dict


def asqk_7g_core(
    query_vector: List[float],
    weights: Optional[List[float]] = None,
    bias: float = 0.0,
    adaptive: bool = False
) -> Dict[str, float | str]:
    """
    ASQK-7G v2 — synteza z wagami, biasem i trybem adaptacyjnym.
    
    Args:
        query_vector: Wektor zapytania (lista wartości float)
        weights: Opcjonalne wagi dla każdego elementu wektora
        bias: Przesunięcie (domyślnie 0.0)
        adaptive: Tryb adaptacyjny (skalowanie przez energię wektora)
    
    Returns:
        Dict z kluczami: status (str), score (float)
    
    Formuła:
        score = (weighted_mean + bias) * factor
        factor: 7.0 (stały) lub dynamiczny (adaptive mode)
    """
    N = len(query_vector)
    
    # Walidacja: pusty wektor
    if N == 0:
        return {"status": "Pusty Wektor", "score": 0.0}
    
    # Walidacja: niezgodne wymiary wag
    if weights is not None and len(weights) != N:
        return {"status": "Błąd: Niezgodne wymiary", "score": 0.0}
    
    # Domyślne wagi (równe)
    if weights is None:
        weights = [1.0] * N
    
    # Walidacja: zerowa suma wag
    total_weight = sum(weights)
    if total_weight == 0:
        return {"status": "Błąd: Zerowa suma wag", "score": 0.0}
    
    # Obliczenia: średnia ważona
    weighted_sum = sum(v * w for v, w in zip(query_vector, weights))
    weighted_mean = weighted_sum / total_weight
    
    # Faktor skalowania
    factor = 7.0
    
    # Tryb adaptacyjny: dynamiczne skalowanie
    if adaptive:
        energy = sum(abs(v) for v in query_vector) / N
        factor = 7.0 + (energy * 0.1)
    
    # Wynik końcowy
    syn_score = (weighted_mean + bias) * factor
    
    return {
        "status": "Gotowe",
        "score": syn_score
    }
