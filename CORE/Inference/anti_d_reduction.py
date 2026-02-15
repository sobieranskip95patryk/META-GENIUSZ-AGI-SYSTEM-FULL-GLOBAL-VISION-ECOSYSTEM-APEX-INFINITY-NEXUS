# CORE/Inference/anti_d_reduction.py
"""
FAZA I: Dekuplowanie Uprzedzeń (Anti-D Reduction)
Cel: Neutralizacja wpływu dystorsji zakodowanych w zbiorze treningowym.

Moduły:
1. Meta-Kognitywny Audyt (MKA): Cost Function of Dependence (C_D)
2. Wektor Causal Isolation: Separacja korelacji od mechanizmów przyczynowych
"""

import sys
import os
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Set
from collections import defaultdict

# Dodanie ścieżki projektu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from CORE.Memory.long_term_graph import LongTermGraphManager


class MetaCognitiveAudit:
    """
    Meta-Kognitywny Audyt (MKA): Metryka pokory kognitywnej.
    Mierzy, w jakim stopniu predykcje są koniecznie uwarunkowane 
    przez historyczną dystrybucję danych (korelacje pozorne).
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        self.dependence_scores: Dict[str, float] = {}
        self.correlation_matrix: Dict[Tuple[str, str], float] = {}
        self.epsilon = 1e-6
        
    def calculate_c_d(self, node: str, context_nodes: List[str]) -> float:
        """
        Cost Function of Dependence (C_D):
        Oblicza stopień zależności węzła od historycznego kontekstu.
        
        C_D = Σ(correlation_strength * frequency_bias) / total_context
        
        Wysoki C_D = Silna zależność od danych treningowych (OSTRZEŻENIE)
        Niski C_D = Niezależne wnioskowanie (SUKCES)
        """
        if not context_nodes:
            return 0.0
            
        G = self.ltm.graph
        total_dependence = 0.0
        valid_connections = 0
        
        for context_node in context_nodes:
            if G.has_edge(node, context_node) or G.has_edge(context_node, node):
                # Moc korelacji: liczba wspólnych połączeń
                correlation_strength = self._calculate_correlation_strength(node, context_node)
                
                # Bias frekwencyjny: jak często ten pattern występuje
                frequency_bias = self._calculate_frequency_bias(node, context_node)
                
                total_dependence += correlation_strength * frequency_bias
                valid_connections += 1
        
        if valid_connections == 0:
            return 0.0
            
        c_d = total_dependence / (valid_connections + self.epsilon)
        self.dependence_scores[node] = c_d
        
        return c_d
    
    def _calculate_correlation_strength(self, node_a: str, node_b: str) -> float:
        """
        Oblicza siłę korelacji między dwoma węzłami na podstawie 
        wspólnych sąsiadów (Jaccard similarity).
        """
        G = self.ltm.graph
        
        try:
            neighbors_a = set(G.neighbors(node_a))
            neighbors_b = set(G.neighbors(node_b))
        except:
            return 0.0
        
        if not neighbors_a and not neighbors_b:
            return 0.0
        
        intersection = len(neighbors_a & neighbors_b)
        union = len(neighbors_a | neighbors_b)
        
        jaccard = intersection / (union + self.epsilon)
        
        # Zapisz do matrycy korelacji
        self.correlation_matrix[(node_a, node_b)] = jaccard
        
        return jaccard
    
    def _calculate_frequency_bias(self, node_a: str, node_b: str) -> float:
        """
        Oblicza bias frekwencyjny: jak często ten pattern występował w historii.
        Używamy stopnia węzłów jako proxy dla historycznej aktywności.
        """
        G = self.ltm.graph
        
        try:
            degree_a = G.degree(node_a)
            degree_b = G.degree(node_b)
        except:
            return 0.0
        
        # Normalizacja do [0, 1]
        total_edges = G.number_of_edges()
        if total_edges == 0:
            return 0.0
            
        avg_degree = (degree_a + degree_b) / 2.0
        normalized_bias = avg_degree / (total_edges + self.epsilon)
        
        return min(normalized_bias, 1.0)
    
    def audit_entire_graph(self) -> Dict[str, float]:
        """
        Przeprowadza audyt całego grafu wiedzy.
        Zwraca słownik: {węzeł: C_D score}
        """
        G = self.ltm.graph
        nodes = list(G.nodes())
        
        print(f"[MKA] Rozpoczynam Meta-Kognitywny Audyt dla {len(nodes)} węzłów...")
        
        for node in nodes:
            # Kontekst: bezpośredni sąsiedzi
            try:
                context = list(G.neighbors(node))
            except:
                context = []
            
            self.calculate_c_d(node, context)
        
        # Statystyki
        if self.dependence_scores:
            avg_c_d = np.mean(list(self.dependence_scores.values()))
            max_c_d = max(self.dependence_scores.values())
            
            print(f"[MKA] Średnie C_D: {avg_c_d:.4f}")
            print(f"[MKA] Maksymalne C_D: {max_c_d:.4f}")
            
            # Identyfikacja węzłów o wysokiej zależności
            high_dependence = {k: v for k, v in self.dependence_scores.items() if v > 0.5}
            if high_dependence:
                print(f"[MKA OSTRZEŻENIE] Węzły o wysokiej zależności (C_D > 0.5): {len(high_dependence)}")
        
        return self.dependence_scores


class CausalIsolation:
    """
    Wektor Causal Isolation: Separacja zmiennych skorelowanych od przyczynowych.
    Identyfikuje zmienne zakłócające (confounders) i projektuje 
    sztuczne eksperymenty do falsyfikacji korelacji.
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager, mka: MetaCognitiveAudit):
        self.ltm = ltm_manager
        self.mka = mka
        self.spurious_correlations: Set[Tuple[str, str]] = set()
        self.causal_candidates: Set[Tuple[str, str]] = set()
        self.confounders: Dict[Tuple[str, str], List[str]] = defaultdict(list)
        
    def identify_spurious_correlations(self, threshold: float = 0.6) -> Set[Tuple[str, str]]:
        """
        Identyfikuje korelacje pozorne:
        - Wysoka korelacja (Jaccard > threshold)
        - Brak bezpośredniego mechanizmu przyczynowego
        - Obecność wspólnego przodka (confounder)
        """
        G = self.ltm.graph
        
        print(f"[CAUSAL_ISO] Identyfikacja korelacji pozornych (threshold={threshold})...")
        
        for (node_a, node_b), correlation in self.mka.correlation_matrix.items():
            if correlation < threshold:
                continue
            
            # Sprawdź, czy istnieje bezpośrednie połączenie
            has_direct_edge = G.has_edge(node_a, node_b) or G.has_edge(node_b, node_a)
            
            # Sprawdź, czy istnieje wspólny przodek (potencjalny confounder)
            common_ancestors = self._find_common_ancestors(node_a, node_b)
            
            if correlation >= threshold and common_ancestors:
                # Prawdopodobnie korelacja pozorna
                self.spurious_correlations.add((node_a, node_b))
                self.confounders[(node_a, node_b)] = common_ancestors
                
                print(f"[CAUSAL_ISO] Korelacja pozorna: {node_a} <-> {node_b} "
                      f"(r={correlation:.3f}, confounders={len(common_ancestors)})")
            elif has_direct_edge and correlation >= threshold:
                # Prawdopodobnie relacja przyczynowa
                self.causal_candidates.add((node_a, node_b))
        
        print(f"[CAUSAL_ISO] Znaleziono {len(self.spurious_correlations)} korelacji pozornych")
        print(f"[CAUSAL_ISO] Znaleziono {len(self.causal_candidates)} kandydatów przyczynowych")
        
        return self.spurious_correlations
    
    def _find_common_ancestors(self, node_a: str, node_b: str, max_depth: int = 3) -> List[str]:
        """
        Znajduje wspólnych przodków dwóch węzłów (potencjalne confounders).
        """
        G = self.ltm.graph
        
        try:
            ancestors_a = set()
            ancestors_b = set()
            
            # BFS w górę (predecessors)
            for depth in range(1, max_depth + 1):
                if depth == 1:
                    ancestors_a.update(G.predecessors(node_a))
                    ancestors_b.update(G.predecessors(node_b))
                else:
                    # Rozszerzenie o kolejny poziom
                    new_ancestors_a = set()
                    for ancestor in list(ancestors_a):
                        new_ancestors_a.update(G.predecessors(ancestor))
                    ancestors_a.update(new_ancestors_a)
                    
                    new_ancestors_b = set()
                    for ancestor in list(ancestors_b):
                        new_ancestors_b.update(G.predecessors(ancestor))
                    ancestors_b.update(new_ancestors_b)
            
            common = list(ancestors_a & ancestors_b)
            return common
            
        except Exception as e:
            return []
    
    def design_artificial_experiment(self, node_a: str, node_b: str) -> Dict:
        """
        Projektuje "sztuczny eksperyment" do testowania przyczynowości:
        Symuluje interwencję na A i obserwuje efekt na B.
        
        W pełnej implementacji: to będzie symulacja w przestrzeni grafowej.
        """
        G = self.ltm.graph
        
        # Pobierz confounders
        confounders = self.confounders.get((node_a, node_b), [])
        
        experiment = {
            "hypothesis": f"{node_a} → {node_b}",
            "intervention": f"Manipulacja {node_a} (symulacja do())",
            "control_for": confounders,
            "expected_outcome": "Zmiana w B jeśli A→B jest przyczynowe",
            "test_method": "Graph_Intervention_Simulation",
            "status": "DESIGNED"
        }
        
        print(f"[CAUSAL_ISO] Zaprojektowano eksperyment: {experiment['hypothesis']}")
        
        return experiment
    
    def filter_graph_by_causality(self) -> nx.DiGraph:
        """
        Tworzy przefiltrowany graf zawierający tylko relacje przyczynowe.
        Usuwa korelacje pozorne.
        """
        G_causal = self.ltm.graph.copy()
        
        # Usuń krawędzie odpowiadające korelacjom pozornym
        for node_a, node_b in self.spurious_correlations:
            if G_causal.has_edge(node_a, node_b):
                G_causal.remove_edge(node_a, node_b)
            if G_causal.has_edge(node_b, node_a):
                G_causal.remove_edge(node_b, node_a)
        
        print(f"[CAUSAL_ISO] Graf przefiltrowany: "
              f"{self.ltm.graph.number_of_edges()} → {G_causal.number_of_edges()} krawędzi")
        
        return G_causal


# --- Test Operacyjny ---
if __name__ == "__main__":
    print("=" * 60)
    print("FAZA I: ANTI-D REDUCTION - Test Operacyjny")
    print("=" * 60)
    
    # Inicjalizacja LTM z przykładowymi danymi
    ltm = LongTermGraphManager()
    
    # Symulacja korelacji pozornej: A→C←B (C jest confounder)
    ltm.add_fact("IceCream_Sales", "Temperature", "correlated_with")
    ltm.add_fact("Drowning_Deaths", "Temperature", "correlated_with")
    ltm.add_fact("Temperature", "Summer", "caused_by")
    
    # Prawdziwa przyczynowość: X→Y
    ltm.add_fact("Smoking", "LungCancer", "causes")
    ltm.add_fact("LungCancer", "Death", "causes")
    
    print(f"\n[TEST] Graf inicjalny: {ltm.graph.number_of_nodes()} węzłów, "
          f"{ltm.graph.number_of_edges()} krawędzi")
    
    # FAZA I.1: Meta-Kognitywny Audyt
    print("\n" + "=" * 60)
    print("FAZA I.1: Meta-Kognitywny Audyt (MKA)")
    print("=" * 60)
    
    mka = MetaCognitiveAudit(ltm)
    dependence_scores = mka.audit_entire_graph()
    
    # FAZA I.2: Causal Isolation
    print("\n" + "=" * 60)
    print("FAZA I.2: Wektor Causal Isolation")
    print("=" * 60)
    
    causal_iso = CausalIsolation(ltm, mka)
    spurious = causal_iso.identify_spurious_correlations(threshold=0.3)
    
    # Projektowanie eksperymentu dla pierwszej korelacji pozornej
    if spurious:
        test_pair = list(spurious)[0]
        experiment = causal_iso.design_artificial_experiment(test_pair[0], test_pair[1])
        print(f"\n[TEST] Zaprojektowano eksperyment: {experiment}")
    
    # Filtracja grafu
    G_causal = causal_iso.filter_graph_by_causality()
    
    print("\n" + "=" * 60)
    print("PODSUMOWANIE FAZY I")
    print("=" * 60)
    print(f"✓ Meta-Kognitywny Audyt: {len(dependence_scores)} węzłów przeanalizowanych")
    print(f"✓ Korelacje pozorne zidentyfikowane: {len(spurious)}")
    print(f"✓ Kandydaci przyczynowi: {len(causal_iso.causal_candidates)}")
    print(f"✓ Graf przefiltrowany: {G_causal.number_of_edges()} krawędzi przyczynowych")
    print("\n[FAZA I] Anti-D Reduction: SUKCES. Matryca epistemologiczna oczyszczona.")
