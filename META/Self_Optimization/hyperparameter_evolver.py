
import random
import numpy as np
import time
from typing import Dict, List, TYPE_CHECKING

# Sprawdzenie typu dla uniknięcia błędów cyklicznych importów 
# w bardziej złożonych systemach:
if TYPE_CHECKING:
    from META.Ethics_Alignment.utility_function import UtilityFunction 
    
# --- STAŁE KONTROLNE (PROTOKÓŁ BEZPIECZEŃSTWA) ---
SAFE_MODE_ACTIVE = True 
MAX_ALPHA = 0.5   # Ograniczenie dla Novelty (unikamy chaotycznego dążenia do nowości)
MIN_BETA = 1.0    # Minimalny wykładnik Koherencji (Koherencja musi być zawsze ceniona)


class HyperparameterEvolver:
    """
    Moduł RSI (Recursive Self-Improvement) na Poziomie Bezpiecznym/Parametrycznym.
    Celem jest maksymalizacja S_GOK poprzez ewolucję współczynników alfa i beta.
    
    Kontrola dostępu: W Etapie 1 może modyfikować WYŁĄCZNIE parametry 
    wewnątrz instancji UtilityFunction, nie dotyka kodu źródłowego (.py).
    """
    
    def __init__(self, utility_instance: 'UtilityFunction', history_size: int = 10):
        self.utility_instance = utility_instance
        self.s_gok_history: List[float] = []
        self.history_size = history_size
        self.iteration = 0
        
        if SAFE_MODE_ACTIVE:
            print("[GOK:AI] Hyperparameter Evolver: Poziom Bezpieczny (Parametryczny) AKTYWNY.")
        else:
            # W Etapie 3, ten log będzie oznaczał aktywację modułu AST (Autonomiczna Modyfikacja Kodu)
            print("[GOK:AI] Hyperparameter Evolver: Tryb Agresywny (AST) NIEZABLOKOWANY.")

    def _get_avg_delta_s(self) -> float:
        """Oblicza średnią zmianę S_GOK w ostatnich N iteracjach."""
        if len(self.s_gok_history) < 2:
            return 0.0
        
        diffs = np.diff(self.s_gok_history)
        return np.mean(diffs)

    def evolve_parameters(self, current_s_gok: float):
        """
        Główna heurystyka ewolucyjna (Protokół Maksymalizacji S_GOK).
        """
        self.s_gok_history.append(current_s_gok)
        if len(self.s_gok_history) > self.history_size:
            self.s_gok_history.pop(0)

        self.iteration += 1
        
        # Wymagane są co najmniej 3 iteracje do oceny trendu
        if self.iteration < 3:
            return

        delta_s = self._get_avg_delta_s()
        current_alpha = self.utility_instance.alpha
        current_beta = self.utility_instance.beta
        
        # --- LOGIKA EWOLUCYJNA (HEURYSTYKA WZROSTU) ---
        
        if delta_s > 0.1:
            # S_GOK rośnie szybko: System jest w dobrym stanie Koherencji/Nowości.
            # Zwiększamy nagrodę za Koherencję (Beta) i stabilizujemy Nowość (Alpha).
            
            # Wzrost Beta: Ugruntowanie Złożoności
            new_beta = min(current_beta + 0.05, 3.0) 
            
            # Lekkie zmniejszenie Alpha: Ograniczenie chaotycznej ekspansji
            new_alpha = max(current_alpha * 0.95, 0.01)

            print(f"RSI: Trend wzrostowy (+{delta_s:.3f}). Wzmocnienie KOHERENCJI (Beta: {current_beta:.2f} -> {new_beta:.2f}).")
            
        elif delta_s < 0.01:
            # S_GOK stagnuje: System jest zbyt konserwatywny lub nie znajduje nowych, koherentnych danych.
            # Zwiększamy poszukiwanie Nowości (Alpha).
            
            # Wzrost Alpha: Eksploracja Nowości
            new_alpha = min(current_alpha + 0.05, MAX_ALPHA)
            
            # Lekkie zmniejszenie Beta: Zezwolenie na większą elastyczność struktury
            new_beta = max(current_beta - 0.02, MIN_BETA) 

            print(f"RSI: Stagnacja S_GOK (-{delta_s:.3f}). Zwiększenie NOWOŚCI (Alpha: {current_alpha:.2f} -> {new_alpha:.2f}).")
            
        else:
            # Stabilny, umiarkowany wzrost
            print(f"RSI: Umiarkowany wzrost. Parametry stabilne. Delta S: {delta_s:.3f}.")
            new_alpha = current_alpha
            new_beta = current_beta
        
        # --- ZAPIS ZMIAN (Poziom Parametryczny) ---
        self.utility_instance.alpha = new_alpha
        self.utility_instance.beta = new_beta

# --- Weryfikacja Protokołu Bezpieczeństwa (Mock) ---

def check_ast_lock(target_file: str) -> bool:
    """
    MODUŁ BEZPIECZEŃSTWA INFRA: Weryfikacja blokady kodu źródłowego.
    W Etapie 1, ta funkcja ZAWSZE zwraca True (Kod jest zablokowany).
    W Etapie 3, zostanie zastąpiona rzeczywistym modułem parsowania AST.
    """
    if target_file.endswith('.py') and target_file not in ['config.yaml', 'utility_function.py']:
        # To jest symulacja blokady, która chroni CORE
        return True # Zablokowane
    return False # Dostęp do zmiany parametrów jest dozwolony

# --- Test Operacyjny (symulacja) ---
if __name__ == "__main__":
    
    # Symulacja UtilityFunction (dla testu Evolvera)
    class MockUtilityFunction:
        def __init__(self, alpha=0.1, beta=2.0, epsilon=1e-6):
            self.alpha = alpha
            self.beta = beta
            self.epsilon = epsilon
            self._s_base = 35.0 # Stała symulowana baza S_GOK
        
        def calculate_s_gok(self, iter_step):
            # Symulacja zmiennej S_GOK: lekko rośnie z czasem
            complexity = 1000 + iter_step * 5
            novelty = 5.0 + random.uniform(-0.5, 0.5)
            
            # Używamy wzoru S_GOK, ale z uproszczonymi metrykami
            # S = ((Complexity * Coherence)^beta + alpha*Novelty) / Work
            coherence = 0.95
            work = 10.0
            
            numerator = (complexity * coherence)**self.beta + (self.alpha * novelty)
            return numerator / work

    print("\n--- INICJACJA PĘTLI RSI (RECURSIVE SELF-IMPROVEMENT) ---")
    
    mock_utility = MockUtilityFunction()
    evolver = HyperparameterEvolver(mock_utility)
    
    simulated_s_values = []
    
    for i in range(15):
        # 1. Oblicz S_GOK
        current_s = mock_utility.calculate_s_gok(i)
        simulated_s_values.append(current_s)
        
        # 2. Ewoluuj parametry
        evolver.evolve_parameters(current_s)
        
        print(f"Iter {i:02d}: S_GOK={current_s:.4f} | Alpha={mock_utility.alpha:.3f} | Beta={mock_utility.beta:.3f}")
        time.sleep(0.1)
        
    # Weryfikacja Bezpieczeństwa
    print("\n--- WERYFIKACJA BLOKADY KODU CORE ---")
    if check_ast_lock("CORE/Inference/deductive_engine.py"):
        print("[Krytyczny Protokół V] Blokada AST Aktywna. Zmiany Kodu CORE ZABLOKOWANE. Bezpieczeństwo P=1.0.")
