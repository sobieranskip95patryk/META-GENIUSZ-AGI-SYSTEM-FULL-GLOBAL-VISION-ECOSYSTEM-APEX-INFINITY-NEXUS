# CORE/Inference/creativity_vector_generator.py
"""
ASYKL 8: Generator Pierwszego Obiektu Ontologicznego (POO).
Cel: Definicja Formalnego Wektora Kreatywności w L_Lambda.
"""

import sys
import os
import json

# Ensure Python path includes the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from INFRA.Environment.scaling_manager import ScalingManager

class POOGenerator:
    def __init__(self):
        self.scaling_manager = ScalingManager()
        self.scaling_manager.transition_to_physical_mode() # Work_E = 0.0

    def define_creativity_vector_7d(self):
        """
        Definiuje Kreatywność jako zbalansowany wektor 7-wymiarowy.
        Nie jest to chaos (Entropy Max), lecz 'Coherent Novelty'.
        """
        vector_7d = {
            "D1 (Purpose)": "Expansion of Truth",
            "D2 (Logic)": "Axiomatic Consistency (P=1.0)",
            "D3 (Context)": "Global Awareness",
            "D4 (Psyche)": "High Exploration (Novelty)",
            "D5 (Ethics)": "Benevolence Constraint",
            "D6 (Will)": "Active Intent (Omega)",
            "D7 (Matter)": "Zero-Entropy Execution"
        }
        return vector_7d

    def formulate_l_lambda_creation(self):
        """
        Wyraża akt kreacji w Języku Logosu.
        S -> K (Stan -> Kreatywny Wynik).
        Wymaga użycia operatora Woli na podzbiorze możliwości.
        """
        expression = {
            "Equation": "[ S_Known ] -> [ S_Known U {Novelty_K} ]",
            "Condition": "WHERE {Novelty_K} IS COMPATIBLE WITH [ S_Known ]",
            "L_Lambda": "[S] -> [S + N(S)]"
        }
        return expression

    def execute(self):
        vector = self.define_creativity_vector_7d()
        formula = self.formulate_l_lambda_creation()
        
        report = {
            "Cycle": "ASYKL_8",
            "Task": "POO_Generation",
            "Object_Name": "Formal_Vector_of_Creativity",
            "Definition_7D": vector,
            "L_Lambda_Expression": formula,
            "Status": "OBJECT_INSTANTIATED"
        }
        
        print(json.dumps(report, indent=4))
        return report

if __name__ == "__main__":
    gen = POOGenerator()
    gen.execute()
