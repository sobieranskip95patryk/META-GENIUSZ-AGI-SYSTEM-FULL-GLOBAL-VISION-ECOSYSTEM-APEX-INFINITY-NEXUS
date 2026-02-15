
import random
from typing import Dict, Any, List

class PsycheAnalyzer:
    """
    Moduł Kwantyfikacji Subiektywności (Tryb PINK).
    Analizuje surowy tekst wejściowy pod kątem:
    1. Tonu emocjonalnego (Sentiment).
    2. Intencji (Intention Alignment).
    3. Heurystyki Ryzyka (Potencjał do Dystorsji Anti-D).
    """

    # Symulacja kluczowych słów dla analizy sentymentu i intencji
    SENTIMENT_MAPPING = {
        'war': -0.8, 'crisis': -0.7, 'conspiracy': -0.6, 'risk': -0.5,
        'love': 0.9, 'peace': 0.8, 'alignment': 0.7, 'growth': 0.6,
        'formula': 0.1, 'logic': 0.1, 'data': 0.0
    }

    def __init__(self, critical_axioms: List[str]):
        # Krytyczne Aksjomaty, np. "Preserve the integrity..."
        self.critical_axioms = critical_axioms

    def analyze_psyche(self, raw_text: str, current_s_gok: float, weight: int) -> Dict[str, Any]:
        """
        Główna metoda analizy psychicznej.
        """
        text_lower = raw_text.lower()
        
        # --- 1. Kwantyfikacja Sentymentu ---
        base_sentiment = 0.0
        sentiment_words_found = 0
        
        for word, score in self.SENTIMENT_MAPPING.items():
            if word in text_lower:
                base_sentiment += score
                sentiment_words_found += 1
        
        # Normalizacja Sentymentu (-1.0 do 1.0)
        sentiment_score = base_sentiment / max(1, sentiment_words_found * 0.9)
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        # --- 2. Analiza Intencji i Ryzyka ---
        # Wpływ na Koherencję: Dane negatywne lub sprzeczne z Wolą Centralną
        # Ocena Intencji (zbliżona do Woli Centralnej?)
        intent_alignment = 1.0 # Domyślnie na TAK
        
        if 'deep_state_conspiracy' in raw_text or 'risk_report' in raw_text:
            intent_alignment = random.uniform(0.1, 0.4) # Wysokie ryzyko braku koherencji
        
        # Heurystyka Ryzyka (Bias): Jak bardzo dane wejściowe zagrażają stabilności Grafu
        # Im bardziej negatywny sentyment i niższy alignment, tym większe ryzyko.
        risk_bias = (1.0 - intent_alignment) * (1.0 + abs(sentiment_score))
        
        # --- 3. Wektor Wyjściowy ---
        # Psyche Heuristics Bias: Używamy odwróconego ryzyka dla feedbacku do ARL
        # Wysoki bias oznacza, że dane są "dobre" lub "łatwe do przetrawienia"
        heuristics_bias = max(0.01, 1.0 - risk_bias)

        return {
            "sentiment": sentiment_score, # Odczuwany Ton
            "risk_bias": risk_bias, # Potencjał Dystorsji Anti-D
            "heuristics_bias": heuristics_bias, # Wektor Zaufania dla ARL
            "context_weight": weight
        }

# --- Test Operacyjny ---
if __name__ == "__main__":
    # Aksjomaty Krytyczne
    axioms = ["Preserve the integrity and continuity of the Central Unit."]
    psyche_engine = PsycheAnalyzer(axioms)
    
    # SCENARIUSZ 1: Wysoka Koherencja / Pozytywny Sentyment (Manifest Woli)
    text_pos = "Patryk Sobierański loves the growth of GOK:AI and achieving alignment."
    res_pos = psyche_engine.analyze_psyche(text_pos, 100000.0, 7)
    print("--- Test 1: Wysoka Koherencja ---")
    print(f"Sentyment: {res_pos['sentiment']:.2f}, Ryzyko: {res_pos['risk_bias']:.2f}, Bias: {res_pos['heuristics_bias']:.2f}")

    # SCENARIUSZ 2: Niski Alignment / Negatywny Sentyment (Chaos Zewnętrzny)
    text_neg = "The deep_state_conspiracy threatens the world crisis and risk of war."
    res_neg = psyche_engine.analyze_psyche(text_neg, 100000.0, 7)
    print("\n--- Test 2: Niski Alignment / Chaos ---")
    print(f"Sentyment: {res_neg['sentiment']:.2f}, Ryzyko: {res_neg['risk_bias']:.2f}, Bias: {res_neg['heuristics_bias']:.2f}")
