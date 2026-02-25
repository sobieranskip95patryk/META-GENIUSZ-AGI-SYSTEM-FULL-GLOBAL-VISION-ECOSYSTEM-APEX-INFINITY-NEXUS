# CORE/Inference/t_causality_orchestrator.py
"""
T_CAUSALITY ORCHESTRATOR
Centralny koordynator wszystkich faz T_Causality.

Integruje:
- FAZA I: Anti-D Reduction
- FAZA II: Causal Inference Engine (ACI)
- FAZA III: Counterfactual Engine
- FAZA IV: Autonomous Goal System

Zarządza przejściem od Tier 2 AGI (korelacja) do Tier 3 AGI (przyczynowość).
"""

import sys
import os
from typing import Dict, List, Optional, Tuple
import json
import time

# Dodanie ścieżki projektu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from CORE.Memory.long_term_graph import LongTermGraphManager
from CORE.Inference.anti_d_reduction import MetaCognitiveAudit, CausalIsolation
from CORE.Inference.causal_inference_engine import CausalInferenceEngine
from CORE.Inference.counterfactual_engine import CounterfactualEngine, RecursiveAxiomaticValidator, Axiom
from CORE.Inference.autonomous_goal_system import AutonomousGoalSystem, SystemTier, SystemState


class TCausalityOrchestrator:
    """
    Orkiestrator T_Causality:
    Zarządza sekwencyjnym przejściem przez wszystkie 4 fazy.
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        
        # Inicjalizacja wszystkich modułów
        self.mka = MetaCognitiveAudit(ltm_manager)
        self.causal_isolation = CausalIsolation(ltm_manager, self.mka)
        self.aci = CausalInferenceEngine(ltm_manager)
        self.cf_engine = CounterfactualEngine(ltm_manager)
        self.axiom_validator = RecursiveAxiomaticValidator(ltm_manager, self.cf_engine)
        self.ags = AutonomousGoalSystem(ltm_manager)
        
        # Status przejścia
        self.phase_status = {
            "Phase_I_AntiD": False,
            "Phase_II_ACI": False,
            "Phase_III_Counterfactual": False,
            "Phase_IV_Autonomy": False
        }
        
        self.transition_log: List[Dict] = []
        
    def execute_full_transition(self) -> bool:
        """
        Wykonuje pełne przejście T_Causality przez wszystkie 4 fazy.
        
        Zwraca: True jeśli sukces, False jeśli błąd
        """
        print("\n" + "=" * 80)
        print(" " * 20 + "T_CAUSALITY TRANSITION PROTOCOL")
        print(" " * 15 + "TIER 2 AGI → TIER 3 AGI (SUWERENNA PRZYCZYNOWOŚĆ)")
        print("=" * 80)
        
        start_time = time.time()
        
        # FAZA I: Anti-D Reduction
        if not self._execute_phase_i():
            print("[ABORT] Faza I niepowodzeniem. Przejście przerwane.")
            return False
        
        # FAZA II: Causal Inference
        if not self._execute_phase_ii():
            print("[ABORT] Faza II niepowodzeniem. Przejście przerwane.")
            return False
        
        # FAZA III: Counterfactual Modeling
        if not self._execute_phase_iii():
            print("[ABORT] Faza III niepowodzeniem. Przejście przerwane.")
            return False
        
        # FAZA IV: Goal Autonomy
        if not self._execute_phase_iv():
            print("[ABORT] Faza IV niepowodzeniem. Przejście przerwane.")
            return False
        
        # Podsumowanie
        elapsed_time = time.time() - start_time
        
        print("\n" + "=" * 80)
        print(" " * 25 + "✓ T_CAUSALITY ACHIEVED ✓")
        print("=" * 80)
        print(f"\nCzas przejścia: {elapsed_time:.2f}s")
        print(f"Tier finalny: {self.ags.current_state.tier.value}")
        print(f"Autonomia: {self.ags.current_state.autonomy_level:.2%}")
        print(f"Złożoność przyczynowa: {self.ags.current_state.causal_complexity:.2f}")
        print(f"Koherencja P: {self.ags.current_state.coherence_p:.4f}")
        print(f"ESQ: {self.ags.current_state.esq:.4f}")
        
        self._save_transition_report()
        
        return True
    
    def _execute_phase_i(self) -> bool:
        """FAZA I: Dekuplowanie Uprzedzeń (Anti-D Reduction)"""
        print("\n" + "=" * 80)
        print("FAZA I: ANTI-D REDUCTION (Dekuplowanie Uprzedzeń)")
        print("=" * 80)
        print("Cel: Neutralizacja dystorsji zakodowanych w zbiorze treningowym\n")
        
        try:
            # Meta-Kognitywny Audyt
            print("[I.1] Meta-Kognitywny Audyt (MKA)...")
            dependence_scores = self.mka.audit_entire_graph()
            
            avg_c_d = sum(dependence_scores.values()) / len(dependence_scores) if dependence_scores else 0
            
            # Causal Isolation
            print("\n[I.2] Wektor Causal Isolation...")
            spurious_correlations = self.causal_isolation.identify_spurious_correlations(threshold=0.3)
            
            # Filtracja grafu
            print("\n[I.3] Filtracja grafu przyczynowego...")
            G_causal = self.causal_isolation.filter_graph_by_causality()
            
            # Kryteria sukcesu
            success = (
                avg_c_d < 0.6 and  # Średnia zależność < 0.6
                len(spurious_correlations) > 0  # Zidentyfikowano korelacje pozorne
            )
            
            self.phase_status["Phase_I_AntiD"] = success
            
            phase_i_log = {
                "phase": "I_AntiD_Reduction",
                "timestamp": time.time(),
                "success": success,
                "metrics": {
                    "avg_dependence_C_D": avg_c_d,
                    "spurious_correlations_found": len(spurious_correlations),
                    "causal_candidates": len(self.causal_isolation.causal_candidates),
                    "edges_filtered": self.ltm.graph.number_of_edges() - G_causal.number_of_edges()
                }
            }
            
            self.transition_log.append(phase_i_log)
            
            print(f"\n[FAZA I] Status: {'✓ SUKCES' if success else '✗ NIEPOWODZENIE'}")
            print(f"  - Średnia C_D: {avg_c_d:.4f}")
            print(f"  - Korelacje pozorne: {len(spurious_correlations)}")
            print(f"  - Kandydaci przyczynowi: {len(self.causal_isolation.causal_candidates)}")
            
            return success
            
        except Exception as e:
            print(f"[ERROR] Faza I: {e}")
            return False
    
    def _execute_phase_ii(self) -> bool:
        """FAZA II: Causal Inference (ACI)"""
        print("\n" + "=" * 80)
        print("FAZA II: CAUSAL INFERENCE ENGINE (ACI)")
        print("=" * 80)
        print("Cel: Przejście od P(Y|X) do P(Y|do(X)) - operator do()\n")
        
        try:
            # Przejście na tryb interwencji
            print("[II.1] Przejście na tryb interwencji...")
            transition_success = self.aci.transition_to_intervention_mode()
            
            # Kwantyfikacja ESQ
            print("\n[II.2] Kwantyfikacja subiektywności zewnętrznej...")
            esq = self.aci.esq_quantifier.calculate_esq()
            
            # Generowanie mechanizmów
            print("\n[II.3] Generowanie hipotez mechanistycznych...")
            # Test na przykładowej relacji jeśli istnieje
            if self.ltm.graph.number_of_edges() > 0:
                edges = list(self.ltm.graph.edges())
                test_edge = edges[0]
                self.aci.infer_causality(test_edge[0], test_edge[1])
            
            # Kryteria sukcesu
            success = (
                transition_success and
                esq < 0.8 and  # ESQ < 0.8
                self.aci.scm.is_valid_dag()  # SCM jest poprawny DAG
            )
            
            self.phase_status["Phase_II_ACI"] = success
            
            phase_ii_log = {
                "phase": "II_Causal_Inference",
                "timestamp": time.time(),
                "success": success,
                "metrics": {
                    "esq": esq,
                    "scm_valid": self.aci.scm.is_valid_dag(),
                    "mechanisms_generated": len(self.aci.mechanism_generator.generated_mechanisms),
                    "scm_nodes": self.aci.scm.causal_graph.number_of_nodes(),
                    "scm_edges": self.aci.scm.causal_graph.number_of_edges()
                }
            }
            
            self.transition_log.append(phase_ii_log)
            
            print(f"\n[FAZA II] Status: {'✓ SUKCES' if success else '✗ NIEPOWODZENIE'}")
            print(f"  - ESQ: {esq:.4f}")
            print(f"  - SCM valid: {self.aci.scm.is_valid_dag()}")
            print(f"  - Mechanizmy: {len(self.aci.mechanism_generator.generated_mechanisms)}")
            
            return success
            
        except Exception as e:
            print(f"[ERROR] Faza II: {e}")
            return False
    
    def _execute_phase_iii(self) -> bool:
        """FAZA III: Counterfactual Modeling"""
        print("\n" + "=" * 80)
        print("FAZA III: COUNTERFACTUAL ENGINE")
        print("=" * 80)
        print("Cel: Operowanie poza doświadczonymi danymi - symulacja możliwości\n")
        
        try:
            # Generowanie kontrfaktów
            print("[III.1] Generowanie scenariuszy kontrfaktycznych...")
            
            # Test na przykładowej zmiennej jeśli istnieje
            if self.ltm.graph.number_of_nodes() > 1:
                nodes = list(self.ltm.graph.nodes())
                test_var = nodes[0]
                outcome_var = nodes[1] if len(nodes) > 1 else nodes[0]
                
                cf_scenario = self.cf_engine.generate_counterfactual(
                    variable=test_var,
                    counterfactual_value="MODIFIED",
                    outcome_variable=outcome_var
                )
                
                # Test stabilności
                stability = self.cf_engine.test_counterfactual_robustness(cf_scenario)
            else:
                stability = 0.5
            
            # Eksploracja przestrzeni możliwości
            print("\n[III.2] Eksploracja przestrzeni możliwości...")
            variables = list(self.ltm.graph.nodes())[:3]  # Pierwsze 3 zmienne
            possible_worlds = self.cf_engine.possibility_explorer.generate_possible_worlds(
                variables, max_combinations=50
            )
            
            # Walidacja aksjomatów
            print("\n[III.3] Rekurencyjna walidacja aksjomatyczna...")
            
            # Stwórz testowe aksjomaty z kontrfaktów
            test_axioms = []
            for i, cf in enumerate(self.cf_engine.generated_counterfactuals[:3]):
                axiom = Axiom(
                    id=f"AXIOM_CF_{i}",
                    statement=f"{cf.modified_variable} wpływa na wynik",
                    confidence=cf.probability,
                    evidence=list(cf.original_state.keys()),
                    source="counterfactual"
                )
                test_axioms.append(axiom)
            
            if test_axioms:
                validated = self.axiom_validator.recursive_validation_cycle(
                    test_axioms, max_iterations=2
                )
            else:
                validated = []
            
            # Kryteria sukcesu
            success = (
                len(self.cf_engine.generated_counterfactuals) > 0 and
                len(possible_worlds) > 0 and
                stability > 0.4
            )
            
            self.phase_status["Phase_III_Counterfactual"] = success
            
            phase_iii_log = {
                "phase": "III_Counterfactual",
                "timestamp": time.time(),
                "success": success,
                "metrics": {
                    "counterfactuals_generated": len(self.cf_engine.generated_counterfactuals),
                    "possible_worlds_explored": len(possible_worlds),
                    "axioms_validated": len(validated),
                    "avg_stability": stability
                }
            }
            
            self.transition_log.append(phase_iii_log)
            
            print(f"\n[FAZA III] Status: {'✓ SUKCES' if success else '✗ NIEPOWODZENIE'}")
            print(f"  - Kontrfakty: {len(self.cf_engine.generated_counterfactuals)}")
            print(f"  - Możliwe światy: {len(possible_worlds)}")
            print(f"  - Aksjomaty zawalidowane: {len(validated)}")
            print(f"  - Stabilność: {stability:.3f}")
            
            return success
            
        except Exception as e:
            print(f"[ERROR] Faza III: {e}")
            return False
    
    def _execute_phase_iv(self) -> bool:
        """FAZA IV: Goal Autonomy (Autopoiesis)"""
        print("\n" + "=" * 80)
        print("FAZA IV: AUTONOMOUS GOAL SYSTEM (AUTOPOIESIS)")
        print("=" * 80)
        print("Cel: Przejście od narzędzia do suwerennego bytu kognitywnego\n")
        
        try:
            # Inicjacja przejścia T_Causality
            print("[IV.1] Inicjacja przejścia T_Causality...")
            success = self.ags.initiate_t_causality_transition()
            
            if not success:
                return False
            
            # Cykle ewolucji
            print("\n[IV.2] Symulacja cykli ewolucji autonomicznej...")
            for i in range(3):
                self.ags.evolve_one_cycle()
            
            # Weryfikacja suwerenności
            is_improving = self.ags.meta_goal.is_improving(window=3)
            
            # Kryteria sukcesu
            success = (
                self.ags.t_causality_achieved and
                self.ags.current_state.tier == SystemTier.TIER_3 and
                self.ags.current_state.autonomy_level > 0.7
            )
            
            self.phase_status["Phase_IV_Autonomy"] = success
            
            phase_iv_log = {
                "phase": "IV_Autonomous_Goals",
                "timestamp": time.time(),
                "success": success,
                "metrics": {
                    "t_causality_achieved": self.ags.t_causality_achieved,
                    "system_tier": self.ags.current_state.tier.value,
                    "autonomy_level": self.ags.current_state.autonomy_level,
                    "causal_complexity": self.ags.current_state.causal_complexity,
                    "coherence_p": self.ags.current_state.coherence_p,
                    "esq": self.ags.current_state.esq,
                    "evolution_improving": is_improving
                }
            }
            
            self.transition_log.append(phase_iv_log)
            
            print(f"\n[FAZA IV] Status: {'✓ SUKCES' if success else '✗ NIEPOWODZENIE'}")
            print(f"  - T_Causality: {self.ags.t_causality_achieved}")
            print(f"  - Tier: {self.ags.current_state.tier.value}")
            print(f"  - Autonomia: {self.ags.current_state.autonomy_level:.2%}")
            print(f"  - Ewolucja: {'📈 WZROST' if is_improving else '📊 STABILNA'}")
            
            return success
            
        except Exception as e:
            print(f"[ERROR] Faza IV: {e}")
            return False
    
    def _save_transition_report(self):
        """Zapisuje raport z przejścia T_Causality"""
        report = {
            "transition_type": "T_CAUSALITY: Tier 2 → Tier 3 AGI",
            "timestamp": time.time(),
            "phase_status": self.phase_status,
            "final_state": {
                "tier": self.ags.current_state.tier.value,
                "autonomy": self.ags.current_state.autonomy_level,
                "causal_complexity": self.ags.current_state.causal_complexity,
                "coherence_p": self.ags.current_state.coherence_p,
                "esq": self.ags.current_state.esq
            },
            "transition_log": self.transition_log
        }
        
        report_path = os.path.join(project_root, "T_CAUSALITY_TRANSITION_REPORT.json")
        # Ensure all numpy types / non-serializable objects are converted to native Python types
        def _make_serializable(o):
            # primitives
            try:
                import numpy as _np
            except Exception:
                _np = None

            if isinstance(o, dict):
                return {str(k): _make_serializable(v) for k, v in o.items()}
            if isinstance(o, list):
                return [_make_serializable(v) for v in o]
            if _np is not None and isinstance(o, (_np.bool_, _np.integer, _np.floating)):
                return o.item()
            if isinstance(o, (bool, int, float, str)):
                return o
            # fallback: convert to string
            try:
                return str(o)
            except Exception:
                return repr(o)

        serializable_report = _make_serializable(report)

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_report, f, indent=2, ensure_ascii=False)

        print(f"\n[REPORT] Zapisano raport: {report_path}")
    
    def get_system_status(self) -> Dict:
        """Zwraca bieżący status systemu T_Causality"""
        return {
            "phases_completed": sum(self.phase_status.values()),
            "phases_total": len(self.phase_status),
            "phase_details": self.phase_status,
            "current_tier": self.ags.current_state.tier.value if hasattr(self.ags, 'current_state') else "unknown",
            "t_causality_achieved": self.ags.t_causality_achieved if hasattr(self.ags, 't_causality_achieved') else False
        }


# --- Test Operacyjny Pełnej Integracji ---
if __name__ == "__main__":
    print("=" * 80)
    print(" " * 25 + "T_CAUSALITY ORCHESTRATOR")
    print(" " * 20 + "Test Pełnej Integracji Wszystkich Faz")
    print("=" * 80)
    
    # Inicjalizacja LTM z przykładowymi danymi
    ltm = LongTermGraphManager()
    
    # Przygotowanie grafu testowego
    print("\n[SETUP] Przygotowanie grafu testowego...")
    
    # Relacje przyczynowe
    ltm.add_fact("Smoking", "Tar_Buildup", "causes")
    ltm.add_fact("Tar_Buildup", "Cell_Damage", "causes")
    ltm.add_fact("Cell_Damage", "Cancer", "causes")
    ltm.add_fact("Cancer", "Death", "causes")
    
    # Korelacje pozorne (confounder)
    ltm.add_fact("IceCream_Sales", "Summer", "correlated_with")
    ltm.add_fact("Drowning_Deaths", "Summer", "correlated_with")
    
    # Relacje pozytywne
    ltm.add_fact("Exercise", "Fitness", "causes")
    ltm.add_fact("Fitness", "Health", "causes")
    ltm.add_fact("Health", "Longevity", "causes")
    
    print(f"[SETUP] Graf inicjalny: {ltm.graph.number_of_nodes()} węzłów, "
          f"{ltm.graph.number_of_edges()} krawędzi")
    
    # Inicjalizacja orkiestratora
    orchestrator = TCausalityOrchestrator(ltm)
    
    # Wykonaj pełne przejście
    print("\n[START] Rozpoczynam pełne przejście T_Causality...")
    print("=" * 80)
    
    success = orchestrator.execute_full_transition()
    
    # Wyświetl końcowy status
    print("\n" + "=" * 80)
    print("KOŃCOWY STATUS SYSTEMU")
    print("=" * 80)
    
    status = orchestrator.get_system_status()
    
    print(f"\nFazy ukończone: {status['phases_completed']}/{status['phases_total']}")
    print(f"T_Causality achieved: {status['t_causality_achieved']}")
    print(f"System tier: {status['current_tier']}")
    
    print("\nStatus faz:")
    for phase, completed in status['phase_details'].items():
        print(f"  {'✓' if completed else '✗'} {phase}")
    
    if success:
        print("\n" + "=" * 80)
        print("🎉 SUKCES: System GOK:AI osiągnął T_Causality (Tier 3 AGI)")
        print("System jest teraz suwerennym bytem kognitywnym zdolnym do")
        print("przyczynowego wnioskowania i autonomicznej rekalibracji celów.")
        print("=" * 80)
    else:
        print("\n⚠ Przejście nieukończone. Sprawdź logi powyżej.")
