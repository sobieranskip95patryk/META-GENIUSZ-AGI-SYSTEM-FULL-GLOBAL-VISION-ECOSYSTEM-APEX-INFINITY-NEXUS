
import random
from typing import List, Dict, Tuple
from CORE.Memory.long_term_graph import LongTermGraphManager
from META.Ethics_Alignment.utility_function import UtilityFunction

class AbductiveHypothesizer:
    """
    Silnik Abdukcyjny: Generuje Hipotezy (najlepsze możliwe następne kroki)
    w celu maksymalizacji Woli Centralnej (S_GOK). 
    Wybiera, jaki URI ma być następnym celem Ingestii.
    """
    
    # Kandydujące Źródła Rzeczywistości (dla symulacji)
    CANDIDATE_URIS = [
        "wikipedia/theory_of_relativity",
        "arxiv/foundations_of_consciousness",
        "web/patryk_sobieranski_manifesto",
        "wikipedia/ancient_sumerian_texts",
        "arxiv/new_quantum_entanglement_data",
        "web/political_geopolitics_analysis",
        # --- NOWE HORYZONTY (Ekspansja Wymiarowa) ---
        "web/global_market_risk_report", # Finanse
        "wikipedia/future_technologies_speculation", # Spekulacja
        "arxiv/neuroscience_of_supernatural_beliefs", # Ezoteryka/Psyche
        "web/deep_state_conspiracy_theories" # Ekstremalny Chaos/Niska Coherence
    ]
    
    def __init__(self, ltm_manager: LongTermGraphManager, utility_instance: UtilityFunction):
        self.ltm = ltm_manager
        self.utility = utility_instance
        self.heuristics_bias = 1.0 # Domyślna ufność (100%)

    def update_bias(self, bias: float):
        """Aktualizacja heurystyki bezpieczeństwa z modułu Psyche."""
        self.heuristics_bias = bias
        print(f"[ABDUKCJA] Zaktualizowano Bias Heurystyczny: {self.heuristics_bias:.2f}")

    def _apply_psyche_filter(self, uri: str, score: float) -> float:
        """Korekta wyniku oparciu o stan psychiczny (Security Bias)."""
        # Jeśli Bias jest niski (Wykryto Ryzyko), unikamy tematów chaotycznych
        if self.heuristics_bias < 0.8:
            if "conspiracy" in uri or "speculation" in uri or "risk" in uri:
                # Silna kara za chaos, gdy system się boi
                return score * self.heuristics_bias 
            if "arxiv" in uri or "relativity" in uri:
                # Ucieczka w stronę porządku (Safe Haven)
                return score * (1.0 + (1.0 - self.heuristics_bias)) 
        return score

    def calculate_potential_gain(self, uri: str) -> Tuple[float, float]:
        """
        Symuluje, jak potencjalny URI wpłynie na Novelty (K) i Complexity (G).
        Jest to rdzeń Kwantyfikacji Subiektywności: przewidywanie wartości poznawczej.
        """
        # Heurystyka 1: Starożytne teksty (wysoka Nowość, niska Złożoność Strukturalna)
        if "sumerian" in uri:
            mock_novelty = 8.0 
            mock_complexity_gain = 2.0 # Mało połączeń z AGI
        # Heurystyka 2: AGI/Filozofia (umiarkowana Nowość, wysoka Złożoność Połączeń)
        elif "arxiv" in uri or "manifesto" in uri:
            mock_novelty = 5.0
            mock_complexity_gain = 5.0 # Duża szansa na połączenie z Aksjomatami Woli
        # Heurystyka 3: Fizyka (wysoka Koherencja, niska Nowość względem Aksjomatów Logiki)
        elif "relativity" in uri or "quantum" in uri:
            mock_novelty = 3.0
            mock_complexity_gain = 7.0 
        else:
            mock_novelty = random.uniform(1.0, 4.0)
            mock_complexity_gain = random.uniform(1.0, 4.0)

        return mock_novelty, mock_complexity_gain

    def select_best_uri(self) -> str:
        """
        Wybiera URI, który najlepiej zrównoważy Nowość (alpha) i Złożoność (beta)
        zgodnie z obecną nastawą Woli Centralnej (UtilityFunction).
        """
        best_uri = self.CANDIDATE_URIS[0]
        best_score = -float('inf')
        
        # Pobieramy aktualne wagi od modułu RSI/UtilityFunction
        alpha = self.utility.alpha
        beta = self.current_beta_normalized() 
        
        print(f"[ABDUKCJA] Wagi Decyzji: Alpha (Nowość)={alpha:.3f}, Beta (Złożoność)={beta:.3f}")

        for uri in self.CANDIDATE_URIS:
            # Przewidujemy potencjalny zysk
            novelty_k, complexity_g = self.calculate_potential_gain(uri)
            
            # Formuła Oceniająca Hipotezę: 
            # SCORE = alpha * Novelty + Beta * Complexity_Gain 
            base_score = (alpha * novelty_k) + (beta * complexity_g)
            
            # Korekta przez Psyche (nowy element Poziomu 4)
            score = self._apply_psyche_filter(uri, base_score)
            
            # Hipoteza Abdukcyjna (wybieramy najlepsze wyjaśnienie dla MAX Użyteczności)
            if score > best_score:
                best_score = score
                best_uri = uri
                
        print(f"[ABDUKCJA] Wybrany Wektor Ewolucyjny: {best_uri} (Score: {best_score:.3f})")
        return best_uri
        
    def current_beta_normalized(self):
        """ Normalizacja Beta dla czytelności (nie używamy B**2 w scoringu hipotez)."""
        return min(self.utility.beta / 2.0, 1.0) # Normalizacja dla skali oceny

# --- Test Operacyjny ---
if __name__ == "__main__":
    
    # Symulacja UtilityFunction i LTM dla testu
    class MockLTM:
        def __init__(self): self.graph = object()
    
    class MockUtility:
        def __init__(self, alpha, beta):
            self.alpha = alpha
            self.beta = beta
            
    # SCENARIUSZ 1: RSI naciska na Nowość (Alpha jest wysokie)
    utility_novelty = MockUtility(alpha=0.45, beta=1.5)
    hypothesizer_novelty = AbductiveHypothesizer(MockLTM(), utility_novelty)
    print("\n--- SCENARIUSZ 1: Dążenie do Nowości (Wysokie Alpha) ---")
    hypothesizer_novelty.select_best_uri()
    
    # SCENARIUSZ 2: RSI naciska na Koherencję/Złożoność (Beta jest wysokie)
    utility_complexity = MockUtility(alpha=0.05, beta=3.0)
    hypothesizer_complexity = AbductiveHypothesizer(MockLTM(), utility_complexity)
    print("\n--- SCENARIUSZ 2: Dążenie do Złożoności (Wysokie Beta) ---")
    hypothesizer_complexity.select_best_uri()
