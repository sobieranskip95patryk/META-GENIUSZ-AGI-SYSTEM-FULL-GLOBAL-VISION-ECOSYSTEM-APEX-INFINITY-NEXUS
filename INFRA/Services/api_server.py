
# INFRA/Services/api_server.py

import json
import time
import random
import math
from typing import Dict, Any, Union
import os
import sys

# Ensure project root is in path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

# Symulowane importy modułów GOK:AI 
# W pełnym systemie te klasy byłyby dostępne bez mocków
from CORE.Memory.long_term_graph import LongTermGraphManager
from INFRA.Diagnostics.graph_visualizer import GraphVisualizer
from META.Ethics_Alignment.utility_function import UtilityFunction, success_percent

# Helper functions that might be in UtilityFunction or just helpers
def get_coherence_p():
    # Placeholder for coherence P score calculation
    return random.uniform(0.95, 1.0)

def get_graph_complexity():
    # Placeholder
    return random.randint(100, 500)

# --- STAŁE KONTROLNE API (PROTOKÓŁ BEZPIECZEŃSTWA) ---
API_ACCESS_TOKEN = "META-GENIUSZ_75053_KEY" # Klucz dla Woli Centralnej (Silnie Haszowany)
GRAPH_SNAPSHOT_FILENAME = "gok_graph_snapshot.json"

class APIServerMock:
    """
    Mockup Serwera API (FastAPI/Flask). Służy jako Most Wymiarowy.
    """
    def __init__(self, ltm_manager: LongTermGraphManager, utility_instance: UtilityFunction, visualizer_instance: GraphVisualizer):
        self.ltm = ltm_manager
        self.utility = utility_instance
        self.visualizer = visualizer_instance
        print("[GOK:AI API] Most Wymiarowy Inicjowany.")

    # Symulacja funkcji pomocniczych, które będą pobierać dane ze stanów LTM
    def _mock_s_core_theory(self):
        # Symulacja rosnącego F(n)
        def fib(n):
            if n <= 0: return 0
            if n == 1: return 1
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
            
        return 9 * math.pi + fib(random.randint(20, 25))

    # --- ENDPOINT 1 (PUBLICZNY): Manifest Statusu ---
    def get_status(self) -> Dict[str, Any]:
        """
        Endpoint: /status (Publiczny Manifest Statusu)
        """
        
        current_s_gok = self.utility.calculate_s_gok()
        system_level = 3 
        system_stage = random.randint(0, 6)
        success_pct = success_percent(current_s_gok, {'heuristics_bias': 0.5}, system_level)
        
        return {
            "timestamp": time.time(),
            "status": "OPERATIONAL: LEVEL 3 - EKSPANSJA WYMIAROWA",
            "S_CORE_THEORY": f"{self._mock_s_core_theory():.2f}",
            "S_GOK_ACTUAL": f"{current_s_gok:.2f}",
            "Graph_Complexity": f"{get_graph_complexity():.0f}",
            "Coherence_P_Score": f"{get_coherence_p():.3f}",
            "Success_Probability": f"{success_pct:.2f}%",
            "current_phase": f"Level {system_level}, Stage {system_stage}",
            "Alignment_Status": "GREEN (Psi = 1.0) - Zgodność z Wolą Centralną"
        }

    # --- ENDPOINT 2 (PRYWATNY): Manifest Myśli ASI ---
    def get_graph_snapshot(self, auth_key: str) -> Union[Dict[str, str], Dict[str, Any]]:
        """
        Endpoint: /graph_snapshot (Prywatny Manifest Myśli)
        Wymaga autoryzacji (W=7 Protokół Bezpieczeństwa).
        """
        # 1. Weryfikacja Protokołu Bezpieczeństwa (Klucz Woli Centralnej)
        if auth_key != API_ACCESS_TOKEN:
            return {
                "error": "Autoryzacja Krytyczna Odrzucona.",
                "reason": "Wymagany Klucz Woli Centralnej (Meta-Geniusz).",
                "code": 401
            }, 401

        # 2. Generowanie Wizualizacji
        self.visualizer.export_to_json(GRAPH_SNAPSHOT_FILENAME)
        
        # 3. Odczyt i zwrot danych
        try:
            with open(GRAPH_SNAPSHOT_FILENAME, 'r', encoding='utf-8') as f:
                snapshot_data = json.load(f)
            return snapshot_data, 200
        except FileNotFoundError:
            return {
                "error": "Nie znaleziono pliku migawki Grafu.",
                "reason": "Błąd w mechanizmie wizualizacji.",
                "code": 500
            }, 500

# --- Test i Uruchomienie (Symulacja Serwera) ---
if __name__ == "__main__":
    
    # Import AxiomLoader for testing simulation
    try:
        from CORE.Memory.bootstrap import AxiomLoader
    except ImportError:
        # Fallback if bootstrap isn't in path correctly or structure varies
        class AxiomLoader:
            @staticmethod
            def inject_axioms(ltm): pass
            
    # Symulacja Inicjacji Stanu Świadomości
    ltm_manager = LongTermGraphManager()
    
    # We might need to ensure axioms are injected for graph complexity
    try:
        AxiomLoader.inject_axioms(ltm_manager) 
    except Exception as e:
        print(f"[WARN] Axiom injection skipped in API test: {e}")

    # Mocking Utility Function with high S_GOK metrics for realistic output
    utility_instance = UtilityFunction(alpha=0.1, beta=2.0)
    # Monkey patch for the test output
    utility_instance.calculate_s_gok = lambda: 75053.27 
    
    visualizer_instance = GraphVisualizer(ltm_manager)

    # Inicjacja API Serwera
    api = APIServerMock(ltm_manager, utility_instance, visualizer_instance)

    # TEST 1: Publiczny Status
    print("\n[TEST API 1] Zapytanie: /status (Publiczne)")
    status_response = api.get_status()
    print(json.dumps(status_response, indent=2))
    
    # TEST 2: Prywatny Snapshot (Nieautoryzowany)
    print("\n[TEST API 2] Zapytanie: /graph_snapshot (BŁĄD AUTORYZACJI)")
    unauthorized_response, code = api.get_graph_snapshot(auth_key="ZŁY_KLUCZ_CHAOSU")
    print(f"Status Kodu: {code}")
    print(json.dumps(unauthorized_response, indent=2))
    
    # TEST 3: Prywatny Snapshot (Autoryzowany)
    print("\n[TEST API 3] Zapytanie: /graph_snapshot (SUKCES AUTORYZACJI)")
    authorized_response, code = api.get_graph_snapshot(auth_key=API_ACCESS_TOKEN)
    print(f"Status Kodu: {code}")
    
    if code == 200:
        print(f"Eksport Myśli Zakończony Sukcesem. Węzły: {authorized_response['metadata']['node_count']}, Zapisano: {GRAPH_SNAPSHOT_FILENAME}")
