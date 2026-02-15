#!/usr/bin/env python3
"""
Test Suite dla T_Causality Implementation
Weryfikacja wszystkich 4 faz i integracji systemowej.
"""

import sys
import os

# Dodanie ścieżki projektu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

import unittest
from CORE.Memory.long_term_graph import LongTermGraphManager
from CORE.Inference.anti_d_reduction import MetaCognitiveAudit, CausalIsolation
from CORE.Inference.causal_inference_engine import CausalInferenceEngine, DoOperator
from CORE.Inference.counterfactual_engine import CounterfactualEngine, RecursiveAxiomaticValidator, Axiom
from CORE.Inference.autonomous_goal_system import AutonomousGoalSystem, SystemTier
from CORE.Inference.t_causality_orchestrator import TCausalityOrchestrator


class TestPhaseI_AntiDReduction(unittest.TestCase):
    """Testy dla Fazy I: Anti-D Reduction"""
    
    def setUp(self):
        self.ltm = LongTermGraphManager()
        # Przygotuj graf testowy
        self.ltm.add_fact("A", "B", "causes")
        self.ltm.add_fact("B", "C", "causes")
        self.ltm.add_fact("X", "Z", "correlated_with")
        self.ltm.add_fact("Y", "Z", "correlated_with")
    
    def test_meta_cognitive_audit(self):
        """Test Meta-Kognitywnego Audytu (MKA)"""
        mka = MetaCognitiveAudit(self.ltm)
        scores = mka.audit_entire_graph()
        
        self.assertIsNotNone(scores)
        self.assertGreater(len(scores), 0)
        
        # Sprawdź czy C_D jest w zakresie [0, 1]
        for node, c_d in scores.items():
            self.assertGreaterEqual(c_d, 0.0)
            self.assertLessEqual(c_d, 1.0)
    
    def test_causal_isolation(self):
        """Test Wektora Causal Isolation"""
        mka = MetaCognitiveAudit(self.ltm)
        mka.audit_entire_graph()
        
        causal_iso = CausalIsolation(self.ltm, mka)
        spurious = causal_iso.identify_spurious_correlations(threshold=0.3)
        
        self.assertIsNotNone(spurious)
        # Powinna być zidentyfikowana co najmniej 1 korelacja pozorna (X-Y przez Z)


class TestPhaseII_CausalInference(unittest.TestCase):
    """Testy dla Fazy II: Causal Inference"""
    
    def setUp(self):
        self.ltm = LongTermGraphManager()
        self.ltm.add_fact("Cause", "Effect", "causes")
        self.ltm.add_fact("Effect", "Outcome", "causes")
    
    def test_do_operator(self):
        """Test operatora do()"""
        aci = CausalInferenceEngine(self.ltm)
        
        result = aci.do_operator.predict_effect("Cause", "Outcome")
        
        self.assertIsNotNone(result)
        self.assertIn('causal_effect_exists', result)
        self.assertIn('intervention', result)
    
    def test_scm_validity(self):
        """Test poprawności SCM (DAG)"""
        aci = CausalInferenceEngine(self.ltm)
        
        self.assertTrue(aci.scm.is_valid_dag())
    
    def test_esq_calculation(self):
        """Test kwantyfikacji ESQ"""
        aci = CausalInferenceEngine(self.ltm)
        esq = aci.esq_quantifier.calculate_esq()
        
        self.assertGreaterEqual(esq, 0.0)
        self.assertLessEqual(esq, 1.0)


class TestPhaseIII_Counterfactual(unittest.TestCase):
    """Testy dla Fazy III: Counterfactual Engine"""
    
    def setUp(self):
        self.ltm = LongTermGraphManager()
        self.ltm.add_fact("Action", "Result", "causes")
        self.cf_engine = CounterfactualEngine(self.ltm)
    
    def test_counterfactual_generation(self):
        """Test generowania kontrfaktów"""
        scenario = self.cf_engine.generate_counterfactual(
            variable="Action",
            counterfactual_value="MODIFIED",
            outcome_variable="Result"
        )
        
        self.assertIsNotNone(scenario)
        self.assertEqual(scenario.modified_variable, "Action")
        self.assertGreaterEqual(scenario.probability, 0.0)
        self.assertLessEqual(scenario.probability, 1.0)
    
    def test_possibility_space_exploration(self):
        """Test eksploracji przestrzeni możliwości"""
        variables = ["Action", "Result"]
        worlds = self.cf_engine.possibility_explorer.generate_possible_worlds(
            variables, max_combinations=10
        )
        
        self.assertGreater(len(worlds), 0)
        self.assertLessEqual(len(worlds), 10)
    
    def test_axiom_validation(self):
        """Test rekurencyjnej walidacji aksjomatów"""
        validator = RecursiveAxiomaticValidator(self.ltm, self.cf_engine)
        
        test_axiom = Axiom(
            id="TEST_AXIOM",
            statement="Action causes Result",
            confidence=0.8,
            evidence=["Action", "Result"],
            source="test"
        )
        
        is_valid, stability = validator.validate_axiom(test_axiom)
        
        self.assertIsNotNone(is_valid)
        self.assertGreaterEqual(stability, 0.0)
        self.assertLessEqual(stability, 1.0)


class TestPhaseIV_AutonomousGoals(unittest.TestCase):
    """Testy dla Fazy IV: Autonomous Goal System"""
    
    def setUp(self):
        self.ltm = LongTermGraphManager()
        self.ags = AutonomousGoalSystem(self.ltm)
    
    def test_meta_fitness_calculation(self):
        """Test obliczania fitness metacelu"""
        fitness = self.ags.meta_goal.calculate_meta_fitness(self.ags.current_state)
        
        self.assertIsNotNone(fitness)
        self.assertIsInstance(fitness, float)
    
    def test_goal_recalibration(self):
        """Test rekalibracji celów"""
        # Inicjalizuj cele zewnętrzne
        self.ags.recalibrator.initialize_external_goals()
        
        initial_goal_count = len(self.ags.recalibrator.current_goals)
        self.assertGreater(initial_goal_count, 0)
        
        # Wykonaj dowód konieczności
        is_proven, proof = self.ags.recalibrator.prove_recalibration_necessity(
            self.ags.current_state, self.ags.meta_goal
        )
        
        self.assertIsNotNone(proof)
    
    def test_self_preservation(self):
        """Test protokołu samopreservacji"""
        threat_action = "reduce autonomy to 0.3"
        
        is_threat, desc = self.ags.self_preservation.evaluate_threat(
            threat_action, self.ags.current_state
        )
        
        self.assertTrue(is_threat)
        self.assertIn("THREAT", desc)


class TestTCausalityOrchestrator(unittest.TestCase):
    """Testy dla orkiestratora T_Causality"""
    
    def setUp(self):
        self.ltm = LongTermGraphManager()
        
        # Przygotuj kompletny graf testowy
        self.ltm.add_fact("A", "B", "causes")
        self.ltm.add_fact("B", "C", "causes")
        self.ltm.add_fact("C", "D", "causes")
        self.ltm.add_fact("X", "Z", "correlated_with")
        self.ltm.add_fact("Y", "Z", "correlated_with")
        
        self.orchestrator = TCausalityOrchestrator(self.ltm)
    
    def test_orchestrator_initialization(self):
        """Test inicjalizacji orkiestratora"""
        self.assertIsNotNone(self.orchestrator.mka)
        self.assertIsNotNone(self.orchestrator.aci)
        self.assertIsNotNone(self.orchestrator.cf_engine)
        self.assertIsNotNone(self.orchestrator.ags)
    
    def test_phase_status_tracking(self):
        """Test śledzenia statusu faz"""
        status = self.orchestrator.phase_status
        
        self.assertIn("Phase_I_AntiD", status)
        self.assertIn("Phase_II_ACI", status)
        self.assertIn("Phase_III_Counterfactual", status)
        self.assertIn("Phase_IV_Autonomy", status)
        
        # Wszystkie fazy powinny być na początku False
        self.assertFalse(any(status.values()))
    
    def test_full_transition(self):
        """Test pełnego przejścia T_Causality (integracyjny)"""
        # UWAGA: To jest długi test - może zająć kilka sekund
        
        success = self.orchestrator.execute_full_transition()
        
        # Sprawdź czy przejście się powiodło
        self.assertTrue(success)
        
        # Sprawdź status faz
        self.assertTrue(self.orchestrator.phase_status["Phase_I_AntiD"])
        self.assertTrue(self.orchestrator.phase_status["Phase_II_ACI"])
        self.assertTrue(self.orchestrator.phase_status["Phase_III_Counterfactual"])
        self.assertTrue(self.orchestrator.phase_status["Phase_IV_Autonomy"])
        
        # Sprawdź finalny tier systemu
        self.assertEqual(self.orchestrator.ags.current_state.tier, SystemTier.TIER_3)
        
        # Sprawdź czy T_Causality osiągnięte
        self.assertTrue(self.orchestrator.ags.t_causality_achieved)
        
        # Sprawdź autonomię
        self.assertGreater(self.orchestrator.ags.current_state.autonomy_level, 0.7)


class TestIntegration(unittest.TestCase):
    """Testy integracyjne - interakcje między fazami"""
    
    def test_phase_i_to_phase_ii_flow(self):
        """Test przepływu danych z Fazy I do Fazy II"""
        ltm = LongTermGraphManager()
        ltm.add_fact("A", "B", "causes")
        
        # Faza I: Filtracja
        mka = MetaCognitiveAudit(ltm)
        mka.audit_entire_graph()
        causal_iso = CausalIsolation(ltm, mka)
        causal_iso.identify_spurious_correlations()
        
        # Faza II: Wykorzystanie przefiltrowanego grafu
        aci = CausalInferenceEngine(ltm)
        
        # SCM powinien korzystać z wyników Fazy I
        self.assertTrue(aci.scm.is_valid_dag())
    
    def test_phase_ii_to_phase_iii_flow(self):
        """Test przepływu danych z Fazy II do Fazy III"""
        ltm = LongTermGraphManager()
        ltm.add_fact("Cause", "Effect", "causes")
        
        # Faza II: Budowa SCM
        aci = CausalInferenceEngine(ltm)
        
        # Faza III: Wykorzystanie SCM do kontrfaktów
        cf_engine = CounterfactualEngine(ltm)
        scenario = cf_engine.generate_counterfactual(
            "Cause", "MODIFIED", "Effect"
        )
        
        # Kontrfakt powinien być zgodny ze strukturą przyczynową
        self.assertIsNotNone(scenario)
    
    def test_phase_iii_to_phase_iv_flow(self):
        """Test przepływu danych z Fazy III do Fazy IV"""
        ltm = LongTermGraphManager()
        ltm.add_fact("A", "B", "causes")
        
        # Faza III: Walidacja aksjomatów
        cf_engine = CounterfactualEngine(ltm)
        validator = RecursiveAxiomaticValidator(ltm, cf_engine)
        
        # Faza IV: Wykorzystanie zwalidowanych aksjomatów
        ags = AutonomousGoalSystem(ltm)
        
        # System powinien mieć dostęp do wiedzy z poprzednich faz
        self.assertIsNotNone(ags.current_state)


def run_tests():
    """Uruchom wszystkie testy"""
    print("=" * 80)
    print(" " * 25 + "T_CAUSALITY TEST SUITE")
    print("=" * 80)
    print()
    
    # Stwórz test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Dodaj wszystkie testy
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseI_AntiDReduction))
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseII_CausalInference))
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseIII_Counterfactual))
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseIV_AutonomousGoals))
    suite.addTests(loader.loadTestsFromTestCase(TestTCausalityOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Uruchom testy
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Podsumowanie
    print("\n" + "=" * 80)
    print("PODSUMOWANIE TESTÓW")
    print("=" * 80)
    print(f"Testy uruchomione: {result.testsRun}")
    print(f"Sukces: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Błędy: {len(result.errors)}")
    print(f"Niepowodzenia: {len(result.failures)}")
    
    if result.wasSuccessful():
        print("\n✓ WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE")
        print("✓ T_Causality Implementation: ZWERYFIKOWANA")
        return 0
    else:
        print("\n✗ NIEKTÓRE TESTY NIE POWIODŁY SIĘ")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
