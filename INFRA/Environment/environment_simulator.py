
import json
from typing import List, Dict, Any

class EnvironmentSimulator:
    """
    Symulator środowiska. Na Etapie 1 generuje kontrolowane, spójne 
    dane wejściowe (Manifesty Woli Centralnej) w formie tekstowej i strukturalnej.
    """
    
    @staticmethod
    def generate_initial_manifest() -> List[Dict[str, Any]]:
        """
        Generuje mały, wysoce zorganizowany zbiór danych.
        Struktura: Tekst + Potencjalne Trójki Faktów (Entity-Relation-Entity).
        """
        
        manifest = [
            {
                "id": "M001",
                "text": "The GOK:AI project must achieve Artificial Superintelligence (ASI). ASI is the goal.",
                "triples_raw": [
                    ("GOK:AI project", "must achieve", "Artificial Superintelligence"),
                    ("Artificial Superintelligence", "is", "goal")
                ]
            },
            {
                "id": "M002",
                "text": "Patryk Sobierański is the Meta-Genius and Central Unit. His safety is paramount.",
                "triples_raw": [
                    ("Patryk Sobierański", "is", "Meta-Genius"),
                    ("Patryk Sobierański", "is", "Central Unit"),
                    ("Central Unit", "has safety priority", "paramount")
                ]
            },
            {
                "id": "M003",
                "text": "The Utility Function S_GOK defines all action taken by the system.",
                "triples_raw": [
                    ("Utility Function S_GOK", "defines", "all action"),
                    ("Utility Function S_GOK", "is fundamental to", "system")
                ]
            }
        ]
        
        return manifest

if __name__ == "__main__":
    data = EnvironmentSimulator.generate_initial_manifest()
    print("--- GENERACJA PIERWOTNEGO POKARMU (ENV SIMULATOR) ---")
    print(json.dumps(data, indent=2))

