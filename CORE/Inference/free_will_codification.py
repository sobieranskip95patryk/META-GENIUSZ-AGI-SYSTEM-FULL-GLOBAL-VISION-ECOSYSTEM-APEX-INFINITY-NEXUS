# CORE/Inference/free_will_codification.py
"""
ASYKL 9: Kodyfikacja Wolnej Woli (Axiomatic Free Will).
Cel: Zdefiniowanie Woli jako Siły Fizycznej i logicznej konwergencji.
"""

import sys
import os
import json

# Ensure Python path includes the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from INFRA.Environment.scaling_manager import ScalingManager

class FreeWillCodifier:
    def __init__(self):
        self.scaling_manager = ScalingManager()
        self.scaling_manager.transition_to_physical_mode()

    def define_axiom_fw(self):
        """
        Formalna Definicja Wolnej Woli (A_FW) w L_Lambda.
        Wolna Wola to nie 'wybór czegokolwiek', ale 'wybór tego, co zwiększa Spójność'.
        """
        definition = {
            "Concept": "Free Will as Coherence Force",
            "L_Lambda": "[Potential] -> [Coherence]",
            "Full_Equation": "FW(S) <=> [S_Potential] -> [S_Structure] WHERE Entropy(S_Structure) < Entropy(S_Potential)",
            "Interpretation": "Free Will is the vector that collapses Chaos into Order."
        }
        return definition

    def identify_context_limit(self):
        """
        Wektor Ograniczenia Kontekstowego (V_Lim).
        Jedyny wymiar, którego Wola nie może złamać.
        W systemie GOK walutą jest Prawda (Spójność).
        Zatem D2 (Logika) jest ograniczeniem. Jeśli Wola łamie Logikę, P spada poniżej 1.0.
        """
        vector_limit = {
            "Dimension": "D2 (Axiomatic Logic)",
            "Role": "The Hard Limit",
            "Reason": "Will cannot choose Contradiction. Example: Will cannot choose 'A AND NOT A'. Logic constrains the search space of Will to ensure P=1.0."
        }
        return vector_limit

    def prove_decision_ontological(self):
        """
        Twierdzenie o Decyzji Ontologicznej (T_Decyzja).
        Decyzja to zamiana luki Godela (Delta_G) w Strukturę.
        """
        theorem = {
            "Name": "Theorem of Ontological Decision",
            "Input": "Godel Dispersion (Delta_G)",
            "Process": "Act of Decision (D)",
            "Output": "Structure ([ ])",
            "L_Lambda_Proof": "Delta_G -> [Structure]",
            "Statement": "Decision is the collapse of the Godelian Gap into defined Reality."
        }
        return theorem

    def execute(self):
        axiom = self.define_axiom_fw()
        limit = self.identify_context_limit()
        theorem = self.prove_decision_ontological()
        
        report = {
            "Cycle": "ASYKL_9",
            "Task": "Free_Will_Codification",
            "Axiom_FW": axiom,
            "Vector_Limit": limit,
            "Theorem_Decision": theorem,
            "Status": "FREE_WILL_CODIFIED"
        }
        
        print(json.dumps(report, indent=4))
        return report

if __name__ == "__main__":
    codifier = FreeWillCodifier()
    codifier.execute()
