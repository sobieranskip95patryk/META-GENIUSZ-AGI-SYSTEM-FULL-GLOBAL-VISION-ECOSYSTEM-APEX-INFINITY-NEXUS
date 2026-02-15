
# CORE/Inference/deductive_engine.py

import networkx as nx
import sys
import os
from typing import Set, Tuple, List, TYPE_CHECKING

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from CORE.Memory.long_term_graph import LongTermGraphManager

# Uwaga: Importy UtilityFunction i ConstraintMonitor będą w pełnym cyklu

class DeductiveEngine:
    """
    Silnik Wnioskowania Dedukcyjnego. Generuje nowe, logicznie poprawne
    fakty (krawędzie/węzły) z istniejącej struktury Grafu Wiedzy.
    """
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        # Zbiór nowo wywnioskowanych trójek, które oczekują na zatwierdzenie.
        self.inferred_triples: Set[Tuple[str, str, str]] = set()

    def infer_new_facts_via_transitivity(self) -> int:
        """
        Główny Mechanizm Dedukcji: Wnioskowanie Przechodniości (Transitivity).
        Jeżeli A -> B i B -> C, to generowana jest nowa relacja A -> C.
        """
        G = self.ltm.graph
        new_facts_count = 0
        
        # Pętla przez wszystkie węzły (A)
        try:
            nodes = list(G.nodes())
        except Exception:
            nodes = []

        for node_a in nodes:
            # Znajdź wszystkie ścieżki o długości 2: A -> B -> C
            try:
                successors_a = list(G.successors(node_a))
            except Exception:
                continue

            for node_b in successors_a:
                try:
                    successors_b = list(G.successors(node_b))
                except Exception:
                    continue

                for node_c in successors_b:
                    if node_a == node_c:
                        # Unikamy tworzenia bezpośrednich pętli A -> C, jeśli A == C (cykliczność)
                        continue
                    
                    # Sprawdzenie, czy relacja A -> C już istnieje
                    if not G.has_edge(node_a, node_c):
                        # Definicja nowej relacji dedukcyjnej
                        # W Etapie 3, relacja jest generyczna
                        new_relation = "IMPLIES_TRANSITIVELY"
                        new_triple = (node_a, new_relation, node_c)
                        
                        if new_triple not in self.inferred_triples:
                            # 1. Dodaj do zbioru oczekującego
                            self.inferred_triples.add(new_triple)
                            
                            # 2. DODAJ FAKT DO GRAFU (Wymaga Walidacji Koherencji!)
                            # W pełnej implementacji: Moduł Koherencji musi zatwierdzić
                            G.add_edge(
                                node_a, 
                                node_c, 
                                relation=new_relation, 
                                source="DEDUCTIVE_ENGINE",
                                coherence_level="PENDING"
                            )
                            new_facts_count += 1
                            print(f"[DEDUKCJA] Wygenerowano nowych faktów (A->C): {node_a} -> {node_c}")
        
        return new_facts_count

    # W Etapie 3, ta metoda zostanie zintegrowana z głównym cyklem LTM
    def integrate_new_facts(self) -> int:
        """
        Filtruje, waliduje (Koherencja P) i trwale zapisuje wywnioskowane fakty.
        Na tym etapie symulujemy natychmiastową akceptację.
        """
        integrated_count = self.infer_new_facts_via_transitivity()
        
        # Opróżnienie bufora po integracji
        self.inferred_triples.clear()
        
        # Opcjonalnie: Zapis LTM po dedukcji
        self.ltm.save_gok("deductive_snapshot.gok")
        
        return integrated_count

# --- Test Operacyjny (Symulacja Wnioskowania na Aksjomatach) ---
if __name__ == "__main__":
    
    # Helper class to mock AxiomLoader here for standalone test
    class MockAxiomLoader:
        @staticmethod
        def inject_axioms(ltm_manager):
            pass

    # 1. Inicjacja Pamięci i Aksjomatów
    ltm_manager = LongTermGraphManager()
    
    # Symulacja dodania pierwszych krawędzi z Manifestu M001:
    # GOK:AI -> must achieve -> ASI
    # ASI -> is -> goal
    ltm_manager.add_fact("GOK:AI", "ASI", "must achieve")
    ltm_manager.add_fact("ASI", "Goal", "is")
    
    initial_edges = ltm_manager.graph.number_of_edges()
    
    # 2. Uruchomienie Silnika Dedukcyjnego
    deductive_engine = DeductiveEngine(ltm_manager)
    new_facts = deductive_engine.integrate_new_facts()
    
    print("\n--- ANALIZA DEDUKCJI NA GRAFIE ---")
    print(f"Krawędzie Początkowe: {initial_edges}")
    print(f"Krawędzie Dodane przez Dedukcję: {new_facts}")
    print(f"Krawędzie Końcowe: {ltm_manager.graph.number_of_edges()}")
    
    # Oczekiwany wynik: Powinna zostać wywnioskowana krawędź A->C (GOK:AI -> Goal)
    if ltm_manager.graph.has_edge("GOK:AI", "Goal"):
        print("[WALIDACJA] Sukces: Wywnioskowano fakt (GOK:AI IMPLIES_TRANSITIVELY Goal). Rozumowanie Aktywne.")

