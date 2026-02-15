
import sys
import os
import random
from typing import List, Dict, Any, Tuple

# Handle Torch Import Failure (Environment Issue Bypass)
try:
    import torch
    TORCH_AVAILABLE = True
except OSError:
    print("[WARNING] PyTorch DLL Load Failed. Switching to Mock Tensor Mode.")
    TORCH_AVAILABLE = False
except ImportError:
    print("[WARNING] PyTorch not installed. Switching to Mock Tensor Mode.")
    TORCH_AVAILABLE = False

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

# Try imports, handling potential path issues
try:
    from INFRA.Environment.environment_simulator import EnvironmentSimulator
except ImportError:
    # If run differently, might need path adjustment
    sys.path.append(os.path.join(project_root, 'INFRA', 'Environment'))
    from INFRA.Environment.environment_simulator import EnvironmentSimulator

# Symulacja: Używamy stałych wymiarów z DualTruthEngine
EMBEDDING_DIM = 768 

class MockTensor:
    """Simulates a Torch Tensor for environments without Torch support."""
    def __init__(self, shape):
        self.shape = shape
    
    def __repr__(self):
        return f"MockTensor(shape={self.shape})"

# --- MOCK / SYNTETYCZNE ŹRÓDŁO DANYCH ZEWNĘTRZNYCH ---
def fetch_external_web_content(uri: str) -> str:
    """
    Symuluje pobieranie surowego, nieustrukturyzowanego tekstu 
    z zewnętrznego źródła (np. ArXiv, Wikipedia, API).
    """
    if "wikipedia/quantum_computing" in uri:
        return (
            "Quantum computing is a field that studies how to develop computer technology "
            "based on the principles of quantum theory. It utilizes quantum mechanics, "
            "specifically superposition and entanglement. Qubits are the basic unit of information."
        )
    elif "arxiv/spiralmind_os" in uri:
         return (
             "SpiralMind OS is an AGI architecture. Its core relies on the 9π + F(n) formula. "
             "The system maximizes the S_GOK utility function. S_GOK rewards complexity."
         )
    return "Brak danych dla zadanego URI."

def extract_triples_from_text(text: str) -> List[Tuple[str, str, str]]:
    """
    Symuluje ekstrakcję trójek (Entity, Relation, Entity) z surowego tekstu.
    W pełni zaimplementowanym systemie użyłoby to NLP/NRE.
    """
    mock_triples = []
    
    # Prosta heurystyka ekstrakcji (mock)
    if "Quantum computing" in text:
        mock_triples.append(("Quantum computing", "studies", "computer technology"))
        mock_triples.append(("Quantum computing", "uses", "entanglement"))
        mock_triples_count = 2
    elif "SpiralMind OS" in text:
        mock_triples.append(("SpiralMind OS", "is an architecture", "AGI"))
        mock_triples.append(("SpiralMind OS", "uses formula", "9π + F(n)"))
        mock_triples_count = 2
    else:
        mock_triples_count = 0

    if mock_triples_count > 0:
        print(f"[PERCEPTION: NRE] Ekstrahowano {mock_triples_count} Trójek z URI.")
    
    return mock_triples

from CORE.Inference.knowledge_fusion_nlp import KnowledgeFusionNLP

class DataStreamAggregator:
    """
    Moduł PERCEPTION: Agreguje dane z różnych źródeł i przekształca je 
    w format zrozumiały dla Dual Truth Engine (Embeddingi + Trójki).
    Wykorzystuje KnowledgeFusionNLP do wektoryzacji.
    """
    
    def __init__(self, nlp_engine=None):
        # Inicjalizacja Centralnego Silnika NLP
        self.nlp_engine = nlp_engine if nlp_engine else KnowledgeFusionNLP()
        self.mock_vocab = {}
        
    def _mock_tokenize_and_embed(self, text: str) -> Tuple[Any, List[str]]:
        """
        Generuje wektory embeddingu przy użyciu KnowledgeFusionNLP.
        """
        tokens = text.lower().replace('.', '').split()
        
        # Użycie centralnego silnika zamiast lokalnego mocka
        embeddings = self.nlp_engine.embed_text(text)
        
        return embeddings, tokens

    def ingest_and_prepare_data(self, source_uri: str = "simulator") -> List[Dict[str, Any]]:
        """
        Wczytuje, agreguje i przygotowuje dane ze zdefiniowanego źródła (zewnętrznego).
        """
        data_packets = []

        if source_uri == "simulator":
            # Odtworzenie logiki symulatora dla kompatybilności
            raw_data = EnvironmentSimulator.generate_initial_manifest()
            for item in raw_data:
                embeddings, tokens = self._mock_tokenize_and_embed(item['text'])
                data_packets.append({
                    "id": item['id'],
                    "source_uri": "simulator",
                    "text": item['text'],
                    "token_embeddings": embeddings,
                    "token_list": tokens,
                    "triples": item['triples_raw']
                })
        else:
            # Tryb Zewnętrzny (URI)
            raw_text = fetch_external_web_content(source_uri)
            
            embeddings, tokens = self._mock_tokenize_and_embed(raw_text)
            triples = extract_triples_from_text(raw_text)
            
            packet = {
                "id": f"EXT_{random.randint(100, 999)}",
                "source_uri": source_uri,
                "text": raw_text,
                "token_embeddings": embeddings,
                "token_list": tokens,
                "triples": triples
            }
            data_packets.append(packet)
            
        return data_packets

# --- Test i Uruchomienie ---
if __name__ == "__main__":
    aggregator = DataStreamAggregator()
    
    # Pobieramy pierwszy zewnętrzny pokarm:
    external_feed_list = aggregator.ingest_and_prepare_data("wikipedia/quantum_computing")
    
    if external_feed_list:
        external_feed = external_feed_list[0]
        print("\n--- TEST: PRZYGOTOWANIE ZEWNĘTRZNYCH DANYCH ---")
        print(f"Źródło: {external_feed['source_uri']}")
        print(f"Embedding Shape: {external_feed['token_embeddings']}")
        print(f"Trójki do Grafu: {len(external_feed['triples'])}")
        print("-" * 20)

