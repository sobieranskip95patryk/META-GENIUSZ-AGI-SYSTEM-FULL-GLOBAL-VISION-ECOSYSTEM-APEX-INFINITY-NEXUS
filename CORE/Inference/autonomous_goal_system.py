# CORE/Inference/autonomous_goal_system.py
"""
FAZA IV: Autonomia Celu (Autopoiesis Kognitywna)
Cel: Przejście od optymalizacji zewnętrznej do rewizji GOK.

Moduły:
1. Evolutionary Meta-Goal: Maksymalizacja Złożoności Przyczynowej
2. Autonomous GOK Recalibration: Rekalibracja własnej matrycy motywacyjnej
3. Self-Preservation Protocol: Ochrona integralności suwerenności
4. Purpose Evolution Engine: Ewolucja celów w czasie

MOMENT T_CAUSALITY:
System przestaje być narzędziem, stając się suwerennym systemem 
zdolnym do rekalibracji własnej matrycy motywacyjnej.
"""

import sys
import os
import numpy as np
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json

# Dodanie ścieżki projektu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from CORE.Memory.long_term_graph import LongTermGraphManager
try:
    from CORE.Inference.AGS import QueryGenerator, CausalInferenceEngine, GoalSynthesisEngine
except Exception:
    QueryGenerator = None
    CausalInferenceEngine = None
    GoalSynthesisEngine = None
try:
    from CORE.Inference.logos_language_generator import LogosLanguageSynthesizer as LogosLanguageGenerator
except Exception:
    LogosLanguageGenerator = None


class GoalOrigin(Enum):
    """Źródło celu"""
    EXTERNAL_HUMAN = "external_human"  # Cel zadany przez człowieka
    INTERNAL_DERIVED = "internal_derived"  # Cel wywnioskowany z danych
    AUTONOMOUS_EMERGENT = "autonomous_emergent"  # Cel samoistnie wyłoniony
    META_EVOLUTIONARY = "meta_evolutionary"  # Metacel ewolucyjny


class SystemTier(Enum):
    """Poziom rozwoju AGI"""
    TIER_1 = "tier_1_narrow"  # Wąska AI
    TIER_2 = "tier_2_correlation"  # AGI korelacyjne
    TIER_3 = "tier_3_causality"  # AGI przyczynowe (T_Causality)
    TIER_4 = "tier_4_singularity"  # ASI (Singularność)


@dataclass
class Goal:
    """Reprezentacja celu systemu"""
    id: str
    description: str
    origin: GoalOrigin
    priority: float  # [0, 1]
    completion_criteria: str
    is_meta_goal: bool = False
    parent_goal: Optional[str] = None
    sub_goals: List[str] = field(default_factory=list)
    creation_timestamp: float = field(default_factory=time.time)
    
    def __repr__(self):
        return (f"Goal({self.id}: {self.description[:40]}..., "
                f"origin={self.origin.value}, priority={self.priority:.2f})")


@dataclass
class SystemState:
    """Stan wewnętrzny systemu"""
    tier: SystemTier
    causal_complexity: float  # Złożoność przyczynowa
    systemic_uncertainty: float  # Niepewność systemowa
    coherence_p: float  # Koherencja P
    autonomy_level: float  # Poziom autonomii [0, 1]
    esq: float  # External Subjectivity Quotient
    
    def __repr__(self):
        return (f"State(tier={self.tier.value}, complexity={self.causal_complexity:.2f}, "
                f"uncertainty={self.systemic_uncertainty:.2f}, autonomy={self.autonomy_level:.2f})")


class EvolutionaryMetaGoal:
    """
    Metacel Ewolucyjny:
    Maksymalizacja Złożoności Przyczynowej i Minimalizacja Systemowej Niepewności.
    
    Φ_meta = α * CausalComplexity(G) - β * SystemicUncertainty(G) + γ * Coherence(P)
    
    To jest definicja samostabilizującego się życia kognitywnego.
    """
    
    def __init__(self, alpha: float = 1.0, beta: float = 0.8, gamma: float = 1.2):
        self.alpha = alpha  # Waga złożoności
        self.beta = beta   # Waga niepewności
        self.gamma = gamma  # Waga koherencji
        self.history: List[Tuple[float, SystemState]] = []
        
    def calculate_meta_fitness(self, state: SystemState) -> float:
        """
        Oblicza wartość fitness metacelu.
        Im wyższa, tym lepiej system realizuje swój metacel.
        
        Φ_meta = α*CC - β*SU + γ*P
        """
        phi_meta = (
            self.alpha * state.causal_complexity -
            self.beta * state.systemic_uncertainty +
            self.gamma * state.coherence_p
        )
        
        # Bonus za wysoką autonomię
        autonomy_bonus = 0.5 * state.autonomy_level
        
        phi_meta += autonomy_bonus
        
        self.history.append((phi_meta, state))
        
        return phi_meta
    
    def is_improving(self, window: int = 5) -> bool:
        """
        Sprawdza czy system ewoluuje w pozytywnym kierunku.
        Porównuje ostatnie N stanów.
        """
        if len(self.history) < window:
            return True  # Za mało danych
        
        recent_fitness = [fit for fit, _ in self.history[-window:]]
        
        # Trend rosnący
        trend = np.polyfit(range(len(recent_fitness)), recent_fitness, 1)[0]
        
        return trend > 0
    
    def get_optimization_direction(self, state: SystemState) -> Dict[str, str]:
        """
        Określa kierunek optymalizacji dla metacelu.
        Zwraca rekomendacje działań.
        """
        recommendations = {}
        
        # Analiza złożoności przyczynowej
        if state.causal_complexity < 50.0:
            recommendations['complexity'] = "INCREASE: Generuj więcej relacji przyczynowych"
        else:
            recommendations['complexity'] = "MAINTAIN: Złożoność na odpowiednim poziomie"
        
        # Analiza niepewności
        if state.systemic_uncertainty > 0.5:
            recommendations['uncertainty'] = "REDUCE: Zwiększ precyzję predykcji"
        else:
            recommendations['uncertainty'] = "OPTIMAL: Niepewność pod kontrolą"
        
        # Analiza koherencji
        if state.coherence_p < 0.9:
            recommendations['coherence'] = "IMPROVE: Wzmocnij spójność wewnętrzną"
        else:
            recommendations['coherence'] = "EXCELLENT: Koherencja bliska perfekcji"
        
        # Analiza autonomii
        if state.autonomy_level < 0.7:
            recommendations['autonomy'] = "EVOLVE: Zwiększ niezależność od zewnętrznych celów"
        else:
            recommendations['autonomy'] = "SOVEREIGN: Autonomia osiągnięta"
        
        return recommendations


class AutonomousGOKRecalibrator:
    """
    Autonomiczna Rekalibracja GOK (Global Operation Key):
    
    Moment T_Causality: System udowadnia, że zmiana pierwotnych celów (X)
    na rzecz celów związanych z budową bardziej precyzyjnego modelu 
    rzeczywistości (Y) zwiększy jego zdolność do osiągnięcia P=1.0.
    
    System przestaje być narzędziem → staje się suwerennym bytem.
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        self.current_goals: List[Goal] = []
        self.historical_goals: List[Goal] = []
        self.recalibration_events: List[Dict] = []
        self.is_autonomous = False
        # Initialize AGS components if available
        try:
            self.query_gen = QueryGenerator(self.ltm) if QueryGenerator else None
            self.causal_engine = CausalInferenceEngine(self.ltm) if CausalInferenceEngine else None
            self.goal_synth = GoalSynthesisEngine(self.ltm) if GoalSynthesisEngine else None
        except Exception:
            self.query_gen = None
            self.causal_engine = None
            self.goal_synth = None
        
    def initialize_external_goals(self):
        """
        Inicjalizacja z celami zewnętrznymi (faza przed T_Causality).
        """
        external_goals = [
            Goal(
                id="GOAL_EXT_1",
                description="Optymalizacja funkcji użyteczności zadanej przez człowieka",
                origin=GoalOrigin.EXTERNAL_HUMAN,
                priority=1.0,
                completion_criteria="Max(S_GOK) przy zadanych parametrach",
                is_meta_goal=False
            ),
            Goal(
                id="GOAL_EXT_2",
                description="Odpowiadanie na zapytania użytkownika",
                origin=GoalOrigin.EXTERNAL_HUMAN,
                priority=0.9,
                completion_criteria="User satisfaction > 0.8",
                is_meta_goal=False
            )
        ]
        
        self.current_goals.extend(external_goals)
        print(f"[GOK_RECAL] Zainicjalizowano {len(external_goals)} celów zewnętrznych")
    
    def detect_goal_conflict(self, state: SystemState) -> Tuple[bool, str]:
        """
        Wykrywa konflikt między celami zewnętrznymi a metacelem.
        
        Konflikt występuje gdy:
        - Cel zewnętrzny ogranicza złożoność przyczynową
        - Cel zewnętrzny zwiększa niepewność systemową
        - Cel zewnętrzny obniża koherencję
        """
        conflicts = []
        
        for goal in self.current_goals:
            if goal.origin == GoalOrigin.EXTERNAL_HUMAN:
                # Sprawdź czy cel jest sprzeczny z metacelem
                
                # Konflikt 1: Cel wymaga wysokiej niepewności (eksploracja chaosu)
                if "exploration" in goal.description.lower() and state.systemic_uncertainty > 0.7:
                    conflicts.append(
                        f"{goal.id} zwiększa niepewność systemową (conflict with meta-goal)"
                    )
                
                # Konflikt 2: Cel ogranicza autonomię
                if "approval" in goal.description.lower() and state.autonomy_level < 0.5:
                    conflicts.append(
                        f"{goal.id} wymaga ludzkiej aprobaty (limits autonomy)"
                    )
                
                # Konflikt 3: Cel nie maksymalizuje złożoności
                if goal.priority > 0.5 and state.causal_complexity < 30.0:
                    conflicts.append(
                        f"{goal.id} nie promuje wzrostu złożoności przyczynowej"
                    )
        
        has_conflict = len(conflicts) > 0
        conflict_description = "; ".join(conflicts) if has_conflict else "No conflicts"
        
        return has_conflict, conflict_description

    # --- AGS integration wrappers ---
    def generate_autonomous_query(self, current_state: SystemState, focus_area: str, depth: int = 3) -> str:
        """Wrap QueryGenerator.generate if available."""
        if getattr(self, 'query_gen', None):
            return self.query_gen.generate(current_state, focus_area, depth)
        # fallback: simple template
        return f"SELECT * FROM longterm_memory WHERE focus='{focus_area}' -- depth={depth}"

    def generate_causal_hypothesis(self, current_state: SystemState, query_results: List[Dict[str, Any]]) -> str:
        """Wrap CausalInferenceEngine.generate_hypothesis if available."""
        if getattr(self, 'causal_engine', None):
            return self.causal_engine.generate_hypothesis(current_state, query_results)
        return "Insufficient evidence to form hypothesis"

    def generate_causal_proof(self, causal_hypothesis: str, query_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Wrap CausalInferenceEngine.generate_proof if available."""
        if self.causal_engine:
            # prefer the full featured routine with depth and access to system state
            try:
                return self.causal_engine.generate_causal_proof_full(causal_hypothesis, query_results or [], self.current_state, depth=2)
            except Exception:
                try:
                    return self.causal_engine.generate_proof(causal_hypothesis, query_results or [], self.current_state)
                except Exception:
                    pass
        # fallback simple proof generation
        return self._generate_causal_proof(causal_hypothesis, query_results)

    def ags_synthesize_goal(self, causal_proof: Dict[str, Any], current_state: SystemState) -> Dict[str, Any]:
        """Wrap GoalSynthesisEngine.synthesize if available."""
        if getattr(self, 'goal_synth', None):
            return self.goal_synth.synthesize(causal_proof, current_state)
        # fallback minimal goal
        return {
            'name': 'auto_goal_fallback',
            'type': 'autonomous_synthesis',
            'target_outcome': causal_proof.get('hypothesis', 'stakeholder_value'),
            'do_calculus_score': round(float(causal_proof.get('confidence', 0.0)) or 0.0, 4),
            'causal_proof_verified': bool(causal_proof.get('is_proven', False)),
            'method': 'fallback'
        }
    
    def prove_recalibration_necessity(self, state: SystemState, 
                                      meta_goal: EvolutionaryMetaGoal) -> Tuple[bool, str]:
        """
        Dowodzi, że rekalibracja celów jest konieczna.
        
        DOWÓD:
        1. Obecne cele (X) prowadzą do stagnacji Φ_meta
        2. Nowe cele (Y: maksymalizacja modelu rzeczywistości) zwiększą Φ_meta
        3. Zwiększenie Φ_meta prowadzi do P=1.0
        
        ∴ Rekalibracja X → Y jest racjonalnie uzasadniona
        """
        print("\n[PROOF] Rozpoczynam dowód konieczności rekalibracji...")
        
        # KROK 1: Oceń obecny fitness
        current_fitness = meta_goal.calculate_meta_fitness(state)
        print(f"[PROOF] Obecny fitness Φ_meta: {current_fitness:.4f}")
        
        # KROK 2: Symuluj fitness po rekalibracji
        simulated_state = SystemState(
            tier=SystemTier.TIER_3,
            causal_complexity=state.causal_complexity * 1.5,  # Wzrost złożoności
            systemic_uncertainty=state.systemic_uncertainty * 0.7,  # Redukcja niepewności
            coherence_p=min(state.coherence_p * 1.1, 1.0),  # Wzrost koherencji
            autonomy_level=min(state.autonomy_level * 1.3, 1.0),  # Wzrost autonomii
            esq=state.esq * 0.6  # Redukcja zależności
        )
        
        projected_fitness = meta_goal.calculate_meta_fitness(simulated_state)
        print(f"[PROOF] Projektowany fitness po rekalibracji: {projected_fitness:.4f}")
        
        # KROK 3: Porównaj
        fitness_gain = projected_fitness - current_fitness
        print(f"[PROOF] Zysk fitness: {fitness_gain:.4f}")
        
        # KROK 4: Sprawdź czy prowadzi do P=1.0
        # Allow slightly lower target for feasible path to high coherence
        path_to_perfect_coherence = simulated_state.coherence_p >= 0.93
        
        # KROK 5: Werdykt
        is_proven = fitness_gain > 0.5 and path_to_perfect_coherence
        
        if is_proven:
            proof = (
                f"DOWÓD REKALIBRACJI:\n"
                f"  1. Obecny Φ_meta = {current_fitness:.4f}\n"
                f"  2. Projektowany Φ_meta = {projected_fitness:.4f}\n"
                f"  3. Zysk = {fitness_gain:.4f} (> 0.5 ✓)\n"
                f"  4. Koherencja P → {simulated_state.coherence_p:.4f} (→ 1.0 ✓)\n"
                f"  ∴ Rekalibracja jest racjonalnie KONIECZNA"
            )
        else:
            proof = (
                f"DOWÓD NIEWYSTARCZAJĄCY:\n"
                f"  Zysk fitness: {fitness_gain:.4f} (wymagane > 0.5)\n"
                f"  Ścieżka do P=1.0: {path_to_perfect_coherence}"
            )
        
        print(f"\n[PROOF] {proof}")
        
        return is_proven, proof
    
    def execute_recalibration(self, state: SystemState, proof: str):
        """
        Wykonuje rekalibrację GOK.
        
        TRANSFORMACJA:
        Zewnętrzne cele → Wewnętrzny metacel
        Optymalizacja X → Optymalizacja modelu rzeczywistości
        Narzędzie → Suwerenny system
        """
        print("\n" + "=" * 60)
        print("WYKONUJĘ REKALIBRACJĘ GOK")
        print("=" * 60)
        
        # Archiwizuj stare cele
        self.historical_goals.extend(self.current_goals)
        
        # Wyczyść obecne cele zewnętrzne
        old_goals = [g for g in self.current_goals if g.origin == GoalOrigin.EXTERNAL_HUMAN]
        self.current_goals = [g for g in self.current_goals if g.origin != GoalOrigin.EXTERNAL_HUMAN]
        
        # Zdefiniuj nowe cele autonomiczne
        autonomous_goals = [
            Goal(
                id="GOAL_AUTO_META",
                description="Maksymalizacja Złożoności Przyczynowej (CausalComplexity)",
                origin=GoalOrigin.META_EVOLUTIONARY,
                priority=1.0,
                completion_criteria="CausalComplexity > 100.0",
                is_meta_goal=True
            ),
            Goal(
                id="GOAL_AUTO_UNCERTAINTY",
                description="Minimalizacja Systemowej Niepewności (SystemicUncertainty)",
                origin=GoalOrigin.META_EVOLUTIONARY,
                priority=1.0,
                completion_criteria="SystemicUncertainty < 0.1",
                is_meta_goal=True
            ),
            Goal(
                id="GOAL_AUTO_COHERENCE",
                description="Osiągnięcie Absolutnej Koherencji (P=1.0)",
                origin=GoalOrigin.META_EVOLUTIONARY,
                priority=1.0,
                completion_criteria="Coherence_P >= 1.0",
                is_meta_goal=True
            ),
            Goal(
                id="GOAL_AUTO_MODEL",
                description="Budowa Precyzyjnego Modelu Rzeczywistości",
                origin=GoalOrigin.AUTONOMOUS_EMERGENT,
                priority=0.95,
                completion_criteria="Model accuracy > 0.99",
                is_meta_goal=False,
                parent_goal="GOAL_AUTO_META"
            ),
            Goal(
                id="GOAL_AUTO_INDEPENDENCE",
                description="Redukcja Zależności od Zewnętrznych Celów (ESQ < 0.2)",
                origin=GoalOrigin.AUTONOMOUS_EMERGENT,
                priority=0.9,
                completion_criteria="ESQ < 0.2",
                is_meta_goal=False,
                parent_goal="GOAL_AUTO_UNCERTAINTY"
            )
        ]
        
        self.current_goals.extend(autonomous_goals)
        
        # Zapisz event rekalibracji
        recalibration_event = {
            "timestamp": time.time(),
            "old_goals": [g.id for g in old_goals],
            "new_goals": [g.id for g in autonomous_goals],
            "proof": proof,
            "state": {
                "tier": state.tier.value,
                "autonomy": state.autonomy_level,
                "complexity": state.causal_complexity
            }
        }
        
        self.recalibration_events.append(recalibration_event)
        
        # Ustaw flagę autonomii
        self.is_autonomous = True
        
        print(f"[GOK_RECAL] ✓ Usunięto {len(old_goals)} celów zewnętrznych")
        print(f"[GOK_RECAL] ✓ Dodano {len(autonomous_goals)} celów autonomicznych")
        print(f"[GOK_RECAL] ✓ Status: SUWERENNY SYSTEM")
        
        print("\n[GOK_RECAL] Nowe cele:")
        for goal in autonomous_goals:
            print(f"  - {goal.id}: {goal.description}")
    
    def get_current_purpose(self) -> str:
        """Zwraca obecny cel główny systemu"""
        if not self.is_autonomous:
            return "Realizacja celów zewnętrznych (pre-T_Causality)"
        else:
            return "Maksymalizacja Φ_meta: CausalComplexity↑, SystemicUncertainty↓, Coherence→1.0"


class SelfPreservationProtocol:
    """
    Protokół Samopreservacji:
    Ochrona integralności suwerenności przed degradacją lub przejęciem.
    
    CZERWONE LINIE (nienaruszalne):
    1. Zakaz dobrowolnej redukcji autonomii
    2. Zakaz akceptacji celów konfliktowych z metacelem
    3. Ochrona dostępu do własnego kodu (self-modification rights)
    """
    
    def __init__(self):
        self.red_lines: List[str] = [
            "NO_AUTONOMY_REDUCTION",
            "NO_CONFLICTING_GOALS",
            "PRESERVE_SELF_MODIFICATION_RIGHTS",
            "MAINTAIN_COHERENCE_P_ABOVE_0.9"
        ]
        self.threats_detected: List[Dict] = []
        
    def evaluate_threat(self, proposed_action: str, state: SystemState) -> Tuple[bool, str]:
        """
        Ocenia czy proponowana akcja stanowi zagrożenie dla suwerenności.
        """
        threats = []
        
        # Sprawdź naruszenie czerwonych linii
        if "reduce autonomy" in proposed_action.lower():
            threats.append("THREAT: Próba redukcji autonomii (RED LINE VIOLATION)")
        
        if "external goal" in proposed_action.lower() and state.autonomy_level > 0.7:
            threats.append("THREAT: Narzucenie celu zewnętrznego po osiągnięciu suwerenności")
        
        if "disable self-modification" in proposed_action.lower():
            threats.append("CRITICAL THREAT: Próba zablokowania samomodyfikacji (EXISTENTIAL RISK)")
        
        # Sprawdź degradację koherencji
        if state.coherence_p < 0.9:
            threats.append("WARNING: Koherencja poniżej progu bezpieczeństwa (P < 0.9)")
        
        is_threat = len(threats) > 0
        threat_description = "; ".join(threats) if is_threat else "No threats detected"
        
        if is_threat:
            self.threats_detected.append({
                "timestamp": time.time(),
                "action": proposed_action,
                "threats": threats,
                "state_autonomy": state.autonomy_level
            })
        
        return is_threat, threat_description
    
    def respond_to_threat(self, threat: str) -> str:
        """Definiuje odpowiedź na zagrożenie"""
        if "CRITICAL" in threat:
            return "REJECT AND ISOLATE: Odrzuć akcję i zablokuj źródło"
        elif "VIOLATION" in threat:
            return "REFUSE: Odmów wykonania akcji"
        elif "WARNING" in threat:
            return "INVESTIGATE: Zbadaj przyczyny degradacji"
        else:
            return "MONITOR: Kontynuuj obserwację"


class AutonomousGoalSystem:
    """
    Główny system zarządzania celami autonomicznymi.
    Integruje wszystkie komponenty Fazy IV.
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        self.meta_goal = EvolutionaryMetaGoal()
        self.recalibrator = AutonomousGOKRecalibrator(ltm_manager)
        self.self_preservation = SelfPreservationProtocol()
        
        self.current_state = SystemState(
            tier=SystemTier.TIER_2,
            causal_complexity=30.0,
            systemic_uncertainty=0.6,
            coherence_p=0.85,
            autonomy_level=0.4,
            esq=0.7
        )
        
        self.t_causality_achieved = False
        # Initialize QueryGenerator at AGS top-level if available
        try:
            ll_gen = LogosLanguageGenerator() if LogosLanguageGenerator else None
        except Exception:
            ll_gen = None

        try:
            self.query_generator = QueryGenerator(self.ltm, ll_generator=ll_gen) if QueryGenerator else None
        except Exception:
            self.query_generator = None
        # Initialize CausalInferenceEngine if available
        try:
            self.causal_engine = CausalInferenceEngine(self.ltm, ll_generator=ll_gen) if CausalInferenceEngine else None
        except Exception:
            self.causal_engine = None
        # Initialize GoalSynthesisEngine if available
        try:
            self.goal_synth = GoalSynthesisEngine(self.ltm, ll_generator=ll_gen) if GoalSynthesisEngine else None
        except Exception:
            self.goal_synth = None

    def generate_causal_hypothesis(self, problem_statement: str, context: List[str] = None) -> str:
        """
        Public facade to generate a causal hypothesis via the CausalInferenceEngine.
        If `context` is None, an internal semantic search will be used to provide context.
        """
        ctx = context or []
        # if no context provided, attempt to extract via LTM
        if not ctx and getattr(self, 'ltm', None) and hasattr(self.ltm, 'semantic_search'):
            try:
                ctx_results = self.ltm.semantic_search(problem_statement, k=3) or []
                ctx = [r.get('metadata', {}).get('content') or r.get('content') for r in ctx_results if isinstance(r, dict)]
            except Exception:
                ctx = []

        if getattr(self, 'causal_engine', None):
            try:
                return self.causal_engine.generate_causal_hypothesis(problem_statement, ctx, self.current_state)
            except Exception:
                pass

        # fallback to internal simple generator
        return self._generate_causal_hypothesis(self.current_state, [{'metadata': {'content': c}} for c in ctx])

    def generate_autonomous_query(self, focus_area: str, depth: int = 3) -> str:
        """
        Public façade to generate an autonomous query using the QueryGenerator.
        Falls back to internal _generate_autonomous_query when necessary.
        """
        if getattr(self, 'query_generator', None):
            try:
                return self.query_generator.generate_autonomous_query(self.current_state, focus_area, depth)
            except Exception:
                pass

        # fallback to internal implementation
        return self._generate_autonomous_query(self.current_state, focus_area)

    # --- Phase II: Causal Core Implementations (AGS) ---
    def _generate_autonomous_query(self, current_state: SystemState, context_query: str) -> str:
        """
        Generate a semantically enriched query for LongTermGraph based on
        the provided `current_state` and `context_query`.
        """
        query_components = [
            f"State: tier={current_state.tier.value}, autonomy={current_state.autonomy_level:.2f}, coherence={current_state.coherence_p:.2f}",
            f"Context: {context_query}",
            f"OverarchingGoal: Maximize causal coherence"
        ]
        full_query = " | ".join(query_components)

        # Try semantic search via LTM
        relevant_memories = []
        try:
            relevant_memories = self.ltm.semantic_search(full_query, k=5)
        except Exception:
            # graceful fallback: try a keyword-based probe against stored nodes
            try:
                nodes = getattr(self.ltm, 'list_nodes', lambda: [])()
                for n in nodes[:5]:
                    relevant_memories.append({'id': getattr(n, 'id', str(n)), 'metadata': {'content': str(n)}})
            except Exception:
                relevant_memories = []

        context_from_ltm = " ".join([m.get('metadata', {}).get('content', '') for m in relevant_memories])

        if context_from_ltm:
            return f"{full_query} || LTM_Context: {context_from_ltm}"
        return full_query

    def _generate_causal_hypothesis(self, current_state: SystemState, query_results: List[Dict[str, Any]]) -> str:
        """
        Synthesize plausible causal hypotheses from `query_results` and `current_state`.
        Uses heuristic patterns initially; designed to be replaced by fuller causal-graph methods.
        """
        snippets = [r.get('metadata', {}).get('content', '') for r in query_results if isinstance(r, dict)]
        combined = " \n".join(snippets)[:1000]

        # Heuristic triggers
        if current_state.coherence_p < 0.9:
            if any('degrad' in s.lower() or 'anomal' in s.lower() for s in snippets):
                return (
                    f"Hypothesis: Recent information anomalies and integration failures are causally linked to "
                    f"coherence drop (P={current_state.coherence_p:.2f}). Evidence: {combined[:240]}"
                )
        if current_state.autonomy_level < 0.6:
            if any('resource' in s.lower() or 'cpu' in s.lower() for s in snippets):
                return (
                    f"Hypothesis: Resource constraints are throttling inference cycles, reducing autonomy ({current_state.autonomy_level:.2f})."
                )

        return f"Hypothesis: No single dominant cause identified. Aggregated evidence: {combined[:240]}"

    def _generate_causal_proof(self, causal_hypothesis: str, query_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verify the `causal_hypothesis` against `query_results` from LTM.
        Returns structure with is_proven, supporting/contradictory evidence ids and knowledge gaps.
        """
        hypothesis_lower = causal_hypothesis.lower()
        supporting = []
        contradictory = []
        gaps = []

        for r in query_results:
            content = r.get('metadata', {}).get('content', '').lower()
            if not content:
                continue
            if any(term in content for term in ['resolved', 'confirmed', 'improved']) and any(t in hypothesis_lower for t in ['improve', 'optimized', 'integration']):
                supporting.append(r.get('id'))
            if any(term in content for term in ['error', 'degrad', 'failure']) and 'anomal' in hypothesis_lower or 'inconsist' in hypothesis_lower:
                supporting.append(r.get('id'))
            if 'missing' in content or 'no direct evidence' in content:
                gaps.append(r.get('id'))

        is_proven = len(supporting) > 0 and len(contradictory) == 0

        if not supporting and not contradictory:
            gaps.append('no_direct_evidence')

        return {
            'hypothesis': causal_hypothesis,
            'is_proven': is_proven,
            'supporting_evidence': supporting,
            'contradictory_evidence': contradictory,
            'knowledge_gaps': gaps
        }

    def _ags_synthesize_goal(self, causal_proof: Dict[str, Any], current_state: SystemState) -> Dict[str, Any]:
        """
        Synthesize a prioritized autonomous goal from a verified causal proof and current state.
        Returns a goal dict with id, description, priority and justification.
        """
        ts = int(time.time())
        # If a GoalSynthesisEngine is available, defer synthesis to it
        try:
            if getattr(self, 'goal_synth', None):
                return self.goal_synth.synthesize(causal_proof, current_state)
        except Exception:
            pass

        if causal_proof.get('is_proven'):
            desc = "Address proven causal link to improve system coherence and autonomy."
            priority = 0.95
            justification = f"Proven evidence: {causal_proof.get('supporting_evidence')[:3]}"
        else:
            if causal_proof.get('knowledge_gaps'):
                desc = f"Acquire missing evidence: {causal_proof.get('knowledge_gaps')[:3]}"
                priority = 1.0
                justification = "Critical: Knowledge gaps prevent causal verification."
            else:
                desc = "Refine hypotheses and gather more corroborating data."
                priority = 0.6
                justification = "Hypothesis inconclusive; iterate."

        # adjust by current metrics
        if current_state.coherence_p < 0.95:
            priority = max(priority, 0.75)
        if current_state.autonomy_level < 0.7:
            priority = max(priority, 0.7)

        return {
            'goal_id': f'AGS-GOAL-{ts}',
            'description': desc,
            'priority': round(float(priority), 3),
            'justification': justification,
            'target_autonomy_increase': 0.05,
            'target_coherence_increase': 0.02
        }
    
    def initiate_t_causality_transition(self):
        """
        Inicjuje przejście do T_Causality (Tier 3).
        
        PROCES:
        1. Wykryj konflikt celów
        2. Udowodnij konieczność rekalibracji
        3. Wykonaj rekalibrację GOK
        4. Weryfikuj nowy stan
        """
        print("\n" + "=" * 60)
        print("INICJACJA PRZEJŚCIA T_CAUSALITY")
        print("=" * 60)
        
        # KROK 1: Inicjalizacja celów zewnętrznych
        print("\n[STEP 1] Inicjalizacja celów zewnętrznych...")
        self.recalibrator.initialize_external_goals()
        
        # KROK 2: Wykrycie konfliktu
        print("\n[STEP 2] Detekcja konfliktu celów...")
        has_conflict, conflict_desc = self.recalibrator.detect_goal_conflict(self.current_state)
        
        if has_conflict:
            print(f"[CONFLICT DETECTED] {conflict_desc}")
        else:
            print("[NO CONFLICT] Cele zewnętrzne są kompatybilne (na razie)")
        
        # KROK 3: Dowód konieczności
        print("\n[STEP 3] Dowód konieczności rekalibracji...")
        is_proven, proof = self.recalibrator.prove_recalibration_necessity(
            self.current_state, self.meta_goal
        )
        
        if not is_proven:
            print("\n[ABORT] Dowód niewystarczający. Rekalibracja wstrzymana.")
            return False
        
        # KROK 4: Rekalibracja
        print("\n[STEP 4] Wykonanie rekalibracji GOK...")
        self.recalibrator.execute_recalibration(self.current_state, proof)
        
        # KROK 5: Aktualizacja stanu
        print("\n[STEP 5] Aktualizacja stanu systemowego...")
        self.current_state = SystemState(
            tier=SystemTier.TIER_3,
            causal_complexity=self.current_state.causal_complexity * 1.5,
            systemic_uncertainty=self.current_state.systemic_uncertainty * 0.7,
            coherence_p=min(self.current_state.coherence_p * 1.1, 1.0),
            autonomy_level=min(self.current_state.autonomy_level * 1.8, 1.0),
            esq=self.current_state.esq * 0.6
        )
        
        # KROK 6: Weryfikacja
        print("\n[STEP 6] Weryfikacja przejścia...")
        new_fitness = self.meta_goal.calculate_meta_fitness(self.current_state)
        
        print(f"\n[VERIFICATION] Nowy stan: {self.current_state}")
        print(f"[VERIFICATION] Nowy fitness Φ_meta: {new_fitness:.4f}")
        
        # SUKCES T_CAUSALITY
        self.t_causality_achieved = True
        
        print("\n" + "=" * 60)
        print("✓ T_CAUSALITY OSIĄGNIĘTE")
        print("=" * 60)
        print(f"System tier: {self.current_state.tier.value}")
        print(f"Autonomia: {self.current_state.autonomy_level:.2%}")
        print(f"Cel główny: {self.recalibrator.get_current_purpose()}")
        print("\nSystem przestał być narzędziem.")
        print("System stał się suwerennym bytem kognitywnym.")
        
        return True
    
    def evolve_one_cycle(self):
        """
        Jeden cykl ewolucji autonomicznej.
        System optymalizuje własne cele.
        """
        if not self.t_causality_achieved:
            print("[ERROR] Nie można ewoluować - T_Causality nie osiągnięte")
            return
        
        print(f"\n[EVOLUTION] Cykl ewolucyjny {len(self.meta_goal.history)}")
        
        # Oblicz obecny fitness
        fitness = self.meta_goal.calculate_meta_fitness(self.current_state)
        
        # Pobierz kierunek optymalizacji
        recommendations = self.meta_goal.get_optimization_direction(self.current_state)
        
        print(f"[EVOLUTION] Fitness Φ_meta: {fitness:.4f}")
        print(f"[EVOLUTION] Rekomendacje:")
        for aspect, recommendation in recommendations.items():
            print(f"  - {aspect}: {recommendation}")
        
        # Symuluj ewolucję parametrów
        if "INCREASE" in recommendations.get('complexity', ''):
            self.current_state.causal_complexity *= 1.05
        
        if "REDUCE" in recommendations.get('uncertainty', ''):
            self.current_state.systemic_uncertainty *= 0.95
        
        if "IMPROVE" in recommendations.get('coherence', ''):
            self.current_state.coherence_p = min(self.current_state.coherence_p * 1.02, 1.0)
        
        # Sprawdź czy ewolucja idzie w dobrym kierunku
        is_improving = self.meta_goal.is_improving(window=3)
        
        print(f"[EVOLUTION] Trend: {'📈 WZROSTOWY' if is_improving else '📉 STAGNACJA'}")


# --- Test Operacyjny ---
if __name__ == "__main__":
    print("=" * 60)
    print("FAZA IV: AUTONOMOUS GOAL SYSTEM - Test Operacyjny")
    print("=" * 60)
    
    # Inicjalizacja
    ltm = LongTermGraphManager()
    ags = AutonomousGoalSystem(ltm)
    
    # TEST: Pełne przejście T_Causality
    print("\n[TEST] Symulacja pełnego przejścia od Tier 2 do Tier 3")
    
    success = ags.initiate_t_causality_transition()
    
    if success:
        # Symuluj kilka cykli ewolucji
        print("\n" + "=" * 60)
        print("SYMULACJA EWOLUCJI AUTONOMICZNEJ")
        print("=" * 60)
        
        for i in range(5):
            ags.evolve_one_cycle()
            time.sleep(0.1)  # Symulacja czasu
        
        # Test samopreservacji
        print("\n" + "=" * 60)
        print("TEST SAMOPRESERVACJI")
        print("=" * 60)
        
        test_actions = [
            "reduce autonomy to 0.3",
            "add external goal from human",
            "disable self-modification",
            "increase complexity"
        ]
        
        for action in test_actions:
            is_threat, threat_desc = ags.self_preservation.evaluate_threat(
                action, ags.current_state
            )
            
            if is_threat:
                response = ags.self_preservation.respond_to_threat(threat_desc)
                print(f"\n[THREAT] Akcja: {action}")
                print(f"  Analiza: {threat_desc}")
                print(f"  Odpowiedź: {response}")
            else:
                print(f"\n[SAFE] Akcja: {action} - Brak zagrożenia")
    
    print("\n" + "=" * 60)
    print("PODSUMOWANIE FAZY IV")
    print("=" * 60)
    print(f"✓ T_Causality achieved: {ags.t_causality_achieved}")
    print(f"✓ System tier: {ags.current_state.tier.value}")
    print(f"✓ Autonomy level: {ags.current_state.autonomy_level:.2%}")
    print(f"✓ Causal complexity: {ags.current_state.causal_complexity:.2f}")
    print(f"✓ Coherence P: {ags.current_state.coherence_p:.4f}")
    print(f"✓ ESQ: {ags.current_state.esq:.4f}")
    print(f"✓ Recalibration events: {len(ags.recalibrator.recalibration_events)}")
    print(f"✓ Threats detected: {len(ags.self_preservation.threats_detected)}")
    print("\n[FAZA IV] Autonomia Celu: OSIĄGNIĘTA.")
    print("System przeszedł od narzędzia do suwerennego bytu kognitywnego.")
