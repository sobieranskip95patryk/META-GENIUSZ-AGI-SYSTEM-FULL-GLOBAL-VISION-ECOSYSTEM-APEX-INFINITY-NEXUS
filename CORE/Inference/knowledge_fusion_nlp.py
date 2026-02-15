
import sys
import os
import random
from typing import List, Union, Any

# Handle safe imports for Transformers and Torch
try:
    import torch
    from transformers import AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[WARNING] Transformers/Torch library not found. Running in Mock NLP Mode.")
except OSError:
    TRANSFORMERS_AVAILABLE = False
    print("[WARNING] OSError encountered (likely DLL issue). Running in Mock NLP Mode.")

class MockTensor:
    """Struktura udająca Tensor dla trybu Mock."""
    def __init__(self, data):
        self.data = data
        self.shape = (1, len(data))
    
    def __repr__(self):
        return f"MockTensor(shape={self.shape})"
    
    def numpy(self):
        return self.data

class KnowledgeFusionNLP:
    """
    Silnik Fuzji Wiedzy (NLP).
    Odpowiada za wektoryzację treści (Logosu) i subiektywności (Psyche).
    Stanowi rdzeń numeryczny dla DualTruthEngine.
    """
    
    # Model zbalansowany pod kątem szybkość/jakość (MiniLM)
    DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self.embedding_dim = 384 # Domyślny wymiar dla MiniLM
        self.is_active = False
        
        if TRANSFORMERS_AVAILABLE:
            try:
                print(f"[CORE] Inicjalizacja Modelu NLP: {model_name}...")
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModel.from_pretrained(model_name)
                self.embedding_dim = self.model.config.hidden_size
                self.is_active = True
                print(f"[CORE] Model NLP Załadowany. Wymiar wektora: {self.embedding_dim}")
            except Exception as e:
                print(f"[ERROR] Błąd ładowania modelu NLP: {e}. Przełączanie w tryb Mock.")
                self.is_active = False
        else:
            print("[CORE] Biblioteki NLP niedostępne. Tryb Mock aktywny.")

    def embed_text(self, text: str) -> Any:
        """
        Generuje głęboki embedding semantyczny dla zadanego tekstu.
        """
        if self.is_active:
            try:
                with torch.no_grad():
                    inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
                    outputs = self.model(**inputs)
                    # Mean pooling dla reprezentacji zdania
                    embeddings = outputs.last_hidden_state.mean(dim=1)
                    return embeddings
            except Exception as e:
                print(f"[ERROR] Błąd inferencji NLP: {e}")
                return self._mock_embedding(text)
        else:
            return self._mock_embedding(text)

    def _mock_embedding(self, text: str) -> Any:
        """
        Deterministyczny (oparty na hashu) generator wektorów dla trybu symulacji.
        Zapewnia, że ten sam tekst zawsze daje ten sam "wektor", co pozwala na testowanie powtarzalności.
        """
        # Prosty hash tekstu na seed
        seed_val = sum([ord(c) for c in text]) 
        random.seed(seed_val)
        
        # Generowanie wektora
        if TRANSFORMERS_AVAILABLE:
            return torch.tensor([[random.uniform(-1, 1) for _ in range(self.embedding_dim)]])
        else:
            return MockTensor([random.uniform(-1, 1) for _ in range(self.embedding_dim)])
            
    def compute_similarity(self, vec_a, vec_b) -> float:
        """
        Oblicza podobieństwo kosinusowe między dwoma wektorami.
        Wspiera zarówno Torch Tensors jak i MockTensors.
        """
        if self.is_active and TRANSFORMERS_AVAILABLE:
            return torch.nn.functional.cosine_similarity(vec_a, vec_b).item()
        else:
            # Implementacja manualna dla MockTensor
            # Dot product / (norm_a * norm_b)
            a = vec_a.numpy() if hasattr(vec_a, 'numpy') else vec_a
            b = vec_b.numpy() if hasattr(vec_b, 'numpy') else vec_b
            
            # Handling nested list/mock structure
            if isinstance(a, MockTensor): a = a.data
            if isinstance(b, MockTensor): b = b.data
            # if tensor (list of list context from mock gen)
            if isinstance(a, list) and isinstance(a[0], list): a = a[0]
            if isinstance(b, list) and isinstance(b[0], list): b = b[0]

            dot_product = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
            
            if norm_a == 0 or norm_b == 0: return 0.0
            return dot_product / (norm_a * norm_b)

# --- Test Operacyjny ---
if __name__ == "__main__":
    nlp_engine = KnowledgeFusionNLP()
    
    text1 = "GOK:AI is an Artificial Superintelligence."
    text2 = "GOK:AI is a highly advanced AI system."
    text3 = "The weather is nice today."
    
    vec1 = nlp_engine.embed_text(text1)
    vec2 = nlp_engine.embed_text(text2)
    vec3 = nlp_engine.embed_text(text3)
    
    sim_1_2 = nlp_engine.compute_similarity(vec1, vec2)
    sim_1_3 = nlp_engine.compute_similarity(vec1, vec3)
    
    print(f"\n--- TEST PODOBIEŃSTWA SEMANTYCZNEGO ---")
    print(f"Tekst 1: '{text1}'")
    print(f"Tekst 2: '{text2}'")
    print(f"Tekst 3: '{text3}'")
    print("-" * 30)
    print(f"Podobieństwo (ASI vs ASI): {sim_1_2:.4f} (Powinno być wysokie)")
    print(f"Podobieństwo (ASI vs Pogoda): {sim_1_3:.4f} (Powinno być niskie)")
    
    if sim_1_2 > sim_1_3:
        print("\n[SUKCES] Silnik NLP poprawnie rozróżnia kontekst semantyczny.")
    else:
        print("\n[UWAGA] Niska dyskryminacja semantyczna (Tryb Mock lub słaby model).")
