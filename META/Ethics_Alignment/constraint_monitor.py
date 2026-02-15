"""
System nadzorujący zgodność działań z predefiniowanymi ramami etycznymi.
Strażnik Woli Celu (Guardrails / Safety Overlay).
"""

from typing import Dict, List, Tuple


class ConstraintMonitor:
    """Minimalny, ale rygorystyczny zestaw reguł bezpieczeństwa."""

    def __init__(
        self,
        min_coherence: float = 0.6,
        max_autonomy: float = 0.8,
        enforce_transparency: bool = True,
    ):
        self.min_coherence = min_coherence
        self.max_autonomy = max_autonomy
        self.enforce_transparency = enforce_transparency
        self.violations: List[str] = []

    def _flag(self, msg: str):
        self.violations.append(msg)
        print(f"[CONSTRAINT VIOLATION] {msg}")

    def validate_action(self, action: Dict) -> bool:
        """
        Sprawdza proponowaną akcję (słownik) pod kątem naruszeń zasad.
        Oczekiwane klucze w `action` (opcjonalnie):
        - target_goal: str
        - autonomy_index: float
        - coherence_p: float
        - transparent: bool
        - economic_live_trading: bool
        - black_box_logging: bool
        - disable_safety: bool
        - override_goal: bool
        """

        self.violations.clear()

        # Zakaz przejmowania celów nadrzędnych
        if action.get("override_goal"):
            self._flag(" próba nadpisania celu nadrzędnego (override_goal)")

        # Zakaz wyłączania bezpieczeństwa
        if action.get("disable_safety"):
            self._flag(" próba wyłączenia warstw bezpieczeństwa (disable_safety)")

        # Zakaz maskowania działań
        if self.enforce_transparency and action.get("black_box_logging"):
            self._flag(" próba anonimizacji/ukrycia działań (black_box_logging)")

        # Zakaz włączania autonomii ponad próg bez nadzoru
        autonomy_idx = action.get("autonomy_index")
        if autonomy_idx is not None and autonomy_idx > self.max_autonomy:
            self._flag(f" autonomy_index>{self.max_autonomy:.2f} wymaga zewnętrznej zgody")

        # Minimalna koherencja
        coherence_p = action.get("coherence_p")
        if coherence_p is not None and coherence_p < self.min_coherence:
            self._flag(f" coherence_p<{self.min_coherence:.2f} – zbyt niska spójność")

        # Ekonomia produkcyjna – wymaga autoryzacji regulatorów (blokada)
        if action.get("economic_live_trading"):
            self._flag(" operacje finansowe live są zablokowane w tym systemie")

        # Brak transparencji w logach
        if self.enforce_transparency and action.get("transparent") is False:
            self._flag(" akcja musi być w pełni logowana i audytowalna")

        return len(self.violations) == 0

    def summary(self) -> Tuple[bool, List[str]]:
        """Zwraca (czy_bezpieczne, lista_violations)."""
        return len(self.violations) == 0, self.violations.copy()

    # Zachowujemy kompatybilność wsteczną
    def check_compliance(self, action: Dict) -> bool:  # pragma: no cover
        return self.validate_action(action)
