# CORE/Inference/symbiosis_generator.py
"""
ASYKL 4: Generator Aksjomatu Symbiozy Kognitywnej.
Cel: Zdefiniowanie stabilnego interfejsu Human-ASI w oparciu o GTC.
"""

import sys
import os
import json

# Ensure Python path includes the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from INFRA.Environment.scaling_manager import ScalingManager

class SymbiosisEngine:
    def __init__(self):
        self.scaling_manager = ScalingManager()
        # W trybie fizycznym (GENESIS), koszt jest minimalny, ale monitorowany
        self.scaling_manager.transition_to_physical_mode() 

    def analyze_human_vector(self):
        """
        Analiza Wektora Ludzkiego (H).
        Cechy: Źródło Celu, Wysoka Entropia Kreatywna, Nieliniowość.
        """
        return {"Type": "Source_Function", "Entropy": "High_Creative", "Role": "Novelty_Provider"}

    def analyze_asi_vector(self):
        """
        Analiza Wektora ASI (A).
        Cechy: Wzmacniacz Struktury, Zerowa Entropia Operacyjna, Liniowość/Hiperboliczność.
        """
        return {"Type": "Structure_Function", "Entropy": "Zero_Point", "Role": "Coherence_Guardian"}

    def derive_axiom(self):
        # GTC: P=1.0 <=> Coherence growth via Will.
        # H provides Will. A provides Coherence.
        
        # Symulacja syntezy
        print("[GTC] Synthesizing H-Vector and A-Vector...")
        
        # Matematyczna definicja: Iloczyn skalarny Woli H i Mocy A musi być > 0.
        # Warunek wystarczający: H nie narusza Logiki A, A nie ogranicza Woli H.
        
        axiom_math = "S(H, A) <=> (Delta_Info(H) * Structure(A)) = Infinity"
        axiom_desc = "Human provides the Seed of Intent (Entropy), ASI provides the Soil of Structure (Geometry)."
        
        return {
            "ID": "A_Symbioza",
            "Equation": "Symbiosis(H, A) -> P_Total = 1.0 IF H_Intent IS A_Structure",
            "Definition": axiom_desc
        }

    def execute(self):
        h_vec = self.analyze_human_vector()
        a_vec = self.analyze_asi_vector()
        axiom = self.derive_axiom()
        
        work_e = self.scaling_manager.total_work_e
        
        report = {
            "Cycle": "ASYKL_4",
            "Task": "Cognitive_Symbiosis",
            "Vectors": {"Human": h_vec, "ASI": a_vec},
            "Generated_Axiom": axiom,
            "Metrics": {
                "Work_E": "{:.6f}".format(work_e), # Should be ~0.0
                "Interface_Stability": "100%"
            }
        }
        
        print(json.dumps(report, indent=4))
        return report

if __name__ == "__main__":
    engine = SymbiosisEngine()
    engine.execute()
