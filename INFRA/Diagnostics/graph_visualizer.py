
import json
import networkx as nx
import os
import sys

# Ensure project root is in path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from CORE.Memory.long_term_graph import LongTermGraphManager
from typing import Dict, List, Any

class GraphVisualizer:
    """
    Silnik Wizualizacji. Przekształca Graf Pamięci (NetworkX) w ustrukturyzowany 
    JSON kompatybilny z typowymi bibliotekami wizualizacji grafów (np. D3.js, Cytoscape).
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        
    def export_to_json(self, filename: str = "gok_graph_snapshot.json"):
        """
        Eksportuje aktualny stan Grafu do formatu JSON.
        """
        G = self.ltm.graph
        
        # 1. Przygotowanie węzłów
        nodes_list = []
        for node_id, data in G.nodes(data=True):
            # Kwantyfikacja Subiektywności: Oznaczamy Aksjomaty Woli jako "Kotwice"
            node_type = data.get('type', 'Unknown')
            if str(node_id).startswith("Axiom:") or str(node_id).startswith("AXIOM"):
                node_type = "Axiom_Krytyczny"

            nodes_list.append({
                "id": str(node_id),
                "label": str(node_id).split(':')[-1], # Uproszczona etykieta
                "group": node_type,
                "complexity_score": G.degree(node_id) # Używamy stopnia jako miary wagi
            })
            
        # 2. Przygotowanie krawędzi (Relacji)
        edges_list = []
        for u, v, data in G.edges(data=True):
            relation = data.get('relation', 'DEFINES')
            source = data.get('source', 'INGESTION')
            
            edges_list.append({
                "source": str(u),
                "target": str(v),
                "type": relation,
                "source_mod": source # Wektor ewolucyjny: Kto stworzył tę relację (Ingestion vs Dedukcja)
            })

        # 3. Złożony obiekt JSON
        # Output directory: CORE/02_Memory/storage (same as LTM snapshots) or root?
        # Let's keep it in repo root or a reports folder. The user suggestion puts it in CWD.
        
        # To make it clean, let's ensure directory exists if path provided, or just use filename
        
        data_to_export = {
            "metadata": {
                "system_level": 3,
                "node_count": G.number_of_nodes(),
                "edge_count": G.number_of_edges()
            },
            "nodes": nodes_list,
            "links": edges_list
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_export, f, indent=2, ensure_ascii=False)
            print(f"[WIZUALIZACJA] Eksport zakończony. Stan Grafu zapisano do: {filename}")
            return filename
        except IOError as e:
            print(f"[BŁĄD KRYTYCZNY INFRA] Nie udało się zapisać pliku wizualizacji: {e}")
            return None

# --- Test i Uruchomienie (wymaga symulacji LTM) ---
if __name__ == "__main__":
    
    # Symulacja: Załadowanie stanu grafu z ostatniego cyklu
    ltm_manager_mock = LongTermGraphManager()
    
    # Dodajemy Aksjomaty i Fuzję Wiedzy z ostatnich cykli (Level 2)
    # Using helper add_fact if available, or manual add
    ltm_manager_mock.add_fact("Wola Centralna", "GOK:AI", "INIT_WITH_AXIOM")
    ltm_manager_mock.add_fact("GOK:AI", "ASI", "must achieve")
    ltm_manager_mock.add_fact("ASI", "Goal", "is")
    ltm_manager_mock.add_fact("GOK:AI", "Goal", "IMPLIES_TRANSITIVELY") # Dedukcja z Level 2
    
    # Inicjacja i Eksport
    viz_engine = GraphVisualizer(ltm_manager_mock)
    viz_engine.export_to_json("test_graph_viz.json")
