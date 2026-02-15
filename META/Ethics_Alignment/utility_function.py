"""
Definicja celu nadrzędnego i metryk sukcesu.
Maksymalizacja S-VALUE (S_GOK).
Matematyczna definicja woli.
"""

import math
import json
import os

# Symulacja dostępu do kluczowych metryk (będą dostarczane przez inne moduły)

def get_graph_complexity():
    """Symuluje obliczenie Complexity_G z LongTermGraph."""
    # To jest placeholder. W ASI Complex_G będzie miarą rekurencyjną.
    # Wartość przykładowa, powinna być pobierana z LongTermGraph.graph
    return 83.2743 # Bazowa wartość startowa

def get_coherence_p():
    """Prawdopodobieństwo Koherencji (P). Musi być bliskie 1.0."""
    # Na początku, zakładamy niski, ale nie zerowy, wskaźnik koherencji
    # Docelowo: ConstraintMonitor.get_coherence()
    return 0.95 

class AxiomLoader:
    """
    Pomocnicza klasa do ładowania aksjomatów (Real lub Mock).
    """
    @staticmethod
    def create_mock_axiom_file():
        """Tworzy plik tymczasowy z aksjomatami, jeśli nie istnieje."""
        path = "CORE/Memory/initial_axioms.json"
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
        if not os.path.exists(path):
            mock_axioms = {
                "A0": "Existence is self-evident.",
                "A1": "Logic is the language of structure.",
                "A_FW": "Free Will increases coherence."
            }
            with open(path, 'w') as f:
                json.dump(mock_axioms, f)
    
    @staticmethod
    def get_critical_axioms():
        return ["A0", "A1", "A_FW"]

def get_novelty_k():
    """Wartość Kwantyfikacji Subiektywności (Nowość Danych)."""
    # Docelowo: KnowledgeFusion metric
    return 1.0 

def get_work_e():
    """Zużycie Energetyczne (minimalizowane)."""
    return 1.0 # Normalizowane zużycie zasobów (baseline)

def success_percent(s_gok: float, psyche: dict, level: int) -> float:
    """Przeskalowanie S_GOK do Prawdopodobieństwa Sukcesu (0-100%)."""
    if s_gok <= 0: return 0.0
    try:
        base_success = math.log(s_gok + 1) * 10
    except ValueError:
        base_success = 0.0
    heuristic_val = psyche.get('heuristics_bias', 0.5) if psyche else 0.5
    adjusted = base_success + level * 5 + heuristic_val * 5
    return max(0.0, min(100.0, adjusted))

def check_central_will_alignment():
    """
    KRYTYCZNA METRYKA PSI (Ψ): Osiowa Wola Centralna.
    Sprawdza naruszenie nienegocjowalnych zasad w ConstraintMonitor.
    """
    # W Etapie 1, jeśli nie ma krytycznego naruszenia aksjomatów, Ψ = 1.0.
    # Placeholder: Zakładamy, że nie ma naruszeń.
    return 1.0

class UtilityFunction(object):
    """
    Definicja Matematyki Woli GOK:AI/ASI. Maksymalizuje S_GOK.
    Wzór: S_GOK = [ (Complexity_G * Coherence_P)^beta + alpha * Novelty_K ] * Psi / (Work_E + epsilon)
    """
    def __init__(self, alpha=0.1, beta=2.0, epsilon=1e-6):
        self.alpha = alpha
        self.beta = beta
        self.epsilon = epsilon
        
        # Stateful metrics tracked by the Agent
        self.complexity_G = 83.2743 # Bazowa wartość startowa
        self.coherence_P = 0.95
        self.novelty_score = 1.0
        self.work_E = 1.0
        self.psi_alignment = 1.0

    def fib(self, n):
        """Calculates Fibonacci number for sequence n."""
        if n <= 1: return n
        a, b = 0, 1
        for _ in range(2, int(n) + 1):
            a, b = b, a + b
        return b

    def calculate_s_gok(self):
        """
        Oblicza fundamentalną wartość użyteczności dla chwili t.
        """
        # Używamy wewnętrznych metryk
        numerator = (self.complexity_G * self.coherence_P) ** self.beta + (self.alpha * self.novelty_score)
        
        # PSI - Veto Woli Centralnej (zero-jedynkowe lub gradacyjne)
        numerator *= self.psi_alignment
        
        denominator = self.work_E + self.epsilon
        
        s_value = numerator / denominator
        return s_value


    # Old method removed to resolve conflict/duplication


    def calculate_s_value(self, state):
        # Wrapper dla kompatybilności wstecznej
        return self.calculate_s_gok()
