"""
Testy jednostkowe dla GlobalVision Analyzer
============================================

Testowanie funkcji analitycznych GIS, PRI, CAF, SPC.
Weryfikacja poprawności obliczeń i rekomendacji.

Autor: META-GENIUSZ® (Patryk Sobierański)
Data: 27 stycznia 2026
"""

import unittest
import json
from datetime import datetime
from CORE.Inference.global_vision_analyzer import (
    GlobalVisionAnalyzer,
    PlanetaryImpactMetrics,
)


class TestPlanetaryImpactMetrics(unittest.TestCase):
    """Testy klasy PlanetaryImpactMetrics."""
    
    def test_metrics_creation(self):
        """Test utworzenia metryki z poprawnymi parametrami."""
        metrics = PlanetaryImpactMetrics(
            local_score=1500.0,
            pri=0.85,
            caf=0.80,
            spc=0.70,
            gis=7500.0,
            project_name="Test Project",
        )
        
        self.assertEqual(metrics.local_score, 1500.0)
        self.assertEqual(metrics.pri, 0.85)
        self.assertEqual(metrics.caf, 0.80)
        self.assertEqual(metrics.gis, 7500.0)
    
    def test_metrics_to_dict(self):
        """Test konwersji metryki do słownika."""
        metrics = PlanetaryImpactMetrics(
            local_score=1500.0,
            pri=0.85,
            caf=0.80,
            spc=0.70,
            gis=7500.0,
            project_name="Test",
        )
        
        d = metrics.to_dict()
        
        self.assertIsInstance(d, dict)
        self.assertIn('local_score', d)
        self.assertIn('gis', d)
        self.assertEqual(d['project_name'], "Test")


class TestGlobalVisionAnalyzer(unittest.TestCase):
    """Testy głównego analizatora GlobalVision."""
    
    def setUp(self):
        """Inicjalizacja przed każdym testem."""
        self.analyzer = GlobalVisionAnalyzer()
    
    # ========== Testy obliczenia GIS ==========
    
    def test_gis_calculation_perfect_scores(self):
        """Test GIS z idealnymi wynikami (wszystkie 1.0)."""
        metrics = self.analyzer.calculate_gis(
            local_score=2000.0,
            pri=1.0,
            caf=1.0,
            spc=1.0,
        )
        
        # GIS powinno być bliskie 10000
        self.assertGreater(metrics.gis, 9900)
        self.assertLessEqual(metrics.gis, 10000)
    
    def test_gis_calculation_zero_scores(self):
        """Test GIS z zerami."""
        metrics = self.analyzer.calculate_gis(
            local_score=0.0,
            pri=0.0,
            caf=0.0,
            spc=0.0,
        )
        
        # GIS powinno być 0
        self.assertEqual(metrics.gis, 0.0)
    
    def test_gis_calculation_mixed_scores(self):
        """Test GIS z mieszanymi wynikami."""
        metrics = self.analyzer.calculate_gis(
            local_score=1751.45,
            pri=0.92,
            caf=0.88,
            spc=0.75,
        )
        
        # GIS powinno być w rozsądnym zakresie
        self.assertGreater(metrics.gis, 7000)
        self.assertLess(metrics.gis, 10000)
        
        # Dokładny test: wzór jest liniowy
        expected_gis = ((0.92 * 0.40) + (0.88 * 0.35) + (0.75 * 0.15) + ((1751.45 / 2000.0) * 0.10)) * 10000
        self.assertAlmostEqual(metrics.gis, expected_gis, places=1)
    
    def test_gis_normalized_local_score(self):
        """Test normalizacji LocalScore."""
        # LocalScore powyżej maksimum powinno być ograniczone
        metrics = self.analyzer.calculate_gis(
            local_score=3000.0,  # Powyżej MAX (2000)
            pri=0.5,
            caf=0.5,
            spc=0.5,
        )
        
        # Powinno być ograniczone do 1.0 w normalizacji
        self.assertLessEqual(metrics.gis, 5500)
    
    # ========== Testy walidacji ==========
    
    def test_invalid_pri_range(self):
        """Test rzucenia błędu dla PRI poza zakresem."""
        with self.assertRaises(ValueError):
            self.analyzer.calculate_gis(
                local_score=1500.0,
                pri=1.5,  # Poza zakresem [0, 1]
                caf=0.5,
                spc=0.5,
            )
    
    def test_invalid_caf_range(self):
        """Test rzucenia błędu dla CAF poza zakresem."""
        with self.assertRaises(ValueError):
            self.analyzer.calculate_gis(
                local_score=1500.0,
                pri=0.5,
                caf=-0.1,  # Poza zakresem [0, 1]
                spc=0.5,
            )
    
    def test_invalid_spc_range(self):
        """Test rzucenia błędu dla SPC poza zakresem."""
        with self.assertRaises(ValueError):
            self.analyzer.calculate_gis(
                local_score=1500.0,
                pri=0.5,
                caf=0.5,
                spc=2.0,  # Poza zakresem [0, 1]
            )
    
    # ========== Testy rekomendacji ==========
    
    def test_recommendation_global_scale(self):
        """Test rekomendacji dla projektu na skalę globalną."""
        metrics = self.analyzer.calculate_gis(
            local_score=1800.0,
            pri=0.95,
            caf=0.92,
            spc=0.90,
            project_name="Global Project",
        )
        
        rec = self.analyzer.get_recommendation(metrics)
        
        self.assertEqual(rec['recommendation_level'], "GLOBAL_SCALE")
        self.assertIn("Global Project", rec['explanation'])
        self.assertGreater(len(rec['action_items']), 0)
    
    def test_recommendation_high_potential(self):
        """Test rekomendacji dla projektu o wysokim potencjale."""
        metrics = self.analyzer.calculate_gis(
            local_score=1400.0,
            pri=0.82,
            caf=0.80,
            spc=0.75,
            project_name="High Potential Project",
        )
        
        rec = self.analyzer.get_recommendation(metrics)
        
        self.assertEqual(rec['recommendation_level'], "HIGH_POTENTIAL")
        self.assertGreater(len(rec['action_items']), 0)
    
    def test_recommendation_local_relevance(self):
        """Test rekomendacji dla projektu o znaczeniu lokalnym."""
        metrics = self.analyzer.calculate_gis(
            local_score=900.0,
            pri=0.65,
            caf=0.60,
            spc=0.55,
            project_name="Local Project",
        )
        
        rec = self.analyzer.get_recommendation(metrics)
        
        self.assertEqual(rec['recommendation_level'], "LOCAL_RELEVANCE")
    
    def test_recommendation_review_needed(self):
        """Test rekomendacji dla projektu wymagającego przeglądu."""
        metrics = self.analyzer.calculate_gis(
            local_score=500.0,
            pri=0.40,
            caf=0.35,
            spc=0.30,
            project_name="Risky Project",
        )
        
        rec = self.analyzer.get_recommendation(metrics)
        
        self.assertEqual(rec['recommendation_level'], "REVIEW_NEEDED")
    
    # ========== Testy ryzyka i synergii ==========
    
    def test_risk_factors_low_pri(self):
        """Test identyfikacji ryzyka dla niskiego PRI."""
        metrics = self.analyzer.calculate_gis(
            local_score=1500.0,
            pri=0.60,  # Poniżej 0.7
            caf=0.80,
            spc=0.70,
        )
        
        rec = self.analyzer.get_recommendation(metrics)
        
        risk_found = any("PRI" in risk or "rezonans" in risk.lower() for risk in rec['risk_factors'])
        self.assertTrue(risk_found)
    
    def test_synergy_opportunities_high_scores(self):
        """Test identyfikacji synergii dla wysokich wyników."""
        metrics = self.analyzer.calculate_gis(
            local_score=1800.0,
            pri=0.88,
            caf=0.88,
            spc=0.85,
        )
        
        rec = self.analyzer.get_recommendation(metrics)
        
        self.assertGreater(len(rec['synergy_opportunities']), 0)
    
    # ========== Testy batch analysis ==========
    
    def test_batch_analyze_empty_list(self):
        """Test batch analysis z pustą listą."""
        with self.assertRaises(ValueError):
            self.analyzer.batch_analyze([])
    
    def test_batch_analyze_single_project(self):
        """Test batch analysis z jednym projektem."""
        projects = [
            {
                'name': 'Project 1',
                'local_score': 1500.0,
                'pri': 0.85,
                'caf': 0.80,
                'spc': 0.75,
                'domain': 'Tech',
            }
        ]
        
        result = self.analyzer.batch_analyze(projects)
        
        self.assertEqual(result['portfolio_size'], 1)
        self.assertEqual(len(result['all_analyses']), 1)
    
    def test_batch_analyze_multiple_projects(self):
        """Test batch analysis z wieloma projektami."""
        projects = [
            {'name': 'P1', 'local_score': 1800.0, 'pri': 0.92, 'caf': 0.88, 'spc': 0.75, 'domain': 'A'},
            {'name': 'P2', 'local_score': 1500.0, 'pri': 0.85, 'caf': 0.80, 'spc': 0.70, 'domain': 'B'},
            {'name': 'P3', 'local_score': 800.0, 'pri': 0.65, 'caf': 0.60, 'spc': 0.55, 'domain': 'C'},
        ]
        
        result = self.analyzer.batch_analyze(projects)
        
        self.assertEqual(result['portfolio_size'], 3)
        self.assertGreater(result['average_gis'], 0)
        self.assertGreater(result['max_gis'], result['min_gis'])
    
    def test_batch_analyze_global_scale_detection(self):
        """Test detektowania projektów na skalę globalną w portfolio."""
        projects = [
            {'name': 'Global', 'local_score': 1900.0, 'pri': 0.95, 'caf': 0.92, 'spc': 0.90, 'domain': 'A'},
            {'name': 'Local', 'local_score': 700.0, 'pri': 0.60, 'caf': 0.55, 'spc': 0.50, 'domain': 'B'},
        ]
        
        result = self.analyzer.batch_analyze(projects)
        
        self.assertGreater(result['projects_for_global_scale'], 0)
        self.assertIn('Global', result['projects_recommended_for_scaling'])
        self.assertNotIn('Local', result['projects_recommended_for_scaling'])
    
    # ========== Testy audytu ==========
    
    def test_audit_log_registration(self):
        """Test rejestracji w log audytu."""
        self.analyzer.calculate_gis(
            local_score=1500.0,
            pri=0.85,
            caf=0.80,
            spc=0.75,
        )
        
        self.assertGreater(len(self.analyzer.analysis_history), 0)
    
    def test_audit_log_validation_warning(self):
        """Test rejestracji ostrzeżeń walidacji."""
        # Wyzwól ostrzeżenie poprzez wartość poza zakresem
        self.analyzer.calculate_gis(
            local_score=3500.0,  # Powyżej MAX
            pri=0.5,
            caf=0.5,
            spc=0.5,
        )
        
        # Powinno być ostrzeżenie w audit_log
        warnings = [log for log in self.analyzer.audit_log if log['type'] == 'WARNING']
        self.assertGreater(len(warnings), 0)
    
    # ========== Testy wag strategicznych ==========
    
    def test_weight_verification(self):
        """Test, że wagi sumują się do 1.0."""
        total_weight = (
            self.analyzer.WEIGHT_PRI +
            self.analyzer.WEIGHT_CAF +
            self.analyzer.WEIGHT_SPC +
            self.analyzer.WEIGHT_LS
        )
        
        self.assertAlmostEqual(total_weight, 1.0, places=10)
    
    def test_weight_transparency(self):
        """Test dostępności wag dla audytu."""
        self.assertEqual(self.analyzer.WEIGHT_PRI, 0.40)
        self.assertEqual(self.analyzer.WEIGHT_CAF, 0.35)
        self.assertEqual(self.analyzer.WEIGHT_SPC, 0.15)
        self.assertEqual(self.analyzer.WEIGHT_LS, 0.10)


class TestIntegrationScenarios(unittest.TestCase):
    """Testy integracyjne — rzeczywiste scenariusze."""
    
    def setUp(self):
        self.analyzer = GlobalVisionAnalyzer()
    
    def test_scenario_education_platform(self):
        """Scenariusz: platforma edukacyjna."""
        metrics = self.analyzer.calculate_gis(
            local_score=1751.45,
            pri=0.92,
            caf=0.88,
            spc=0.75,
            project_name="Cosmic Education Platform",
            domain="Education",
        )
        
        self.assertGreater(metrics.gis, 8500)  # Powinno być na skalę globalną
    
    def test_scenario_bioenergy(self):
        """Scenariusz: bioenergia."""
        metrics = self.analyzer.calculate_gis(
            local_score=1240.30,
            pri=0.85,
            caf=0.92,
            spc=0.88,
            project_name="Bioenergy Microgrids",
            domain="Ecology",
        )
        
        self.assertGreater(metrics.gis, 8500)  # Powinno być na skalę globalną
    
    def test_scenario_portfolio_optimization(self):
        """Scenariusz: optymalizacja portfolio."""
        portfolio = [
            {"name": "Project A", "local_score": 1900.0, "pri": 0.95, "caf": 0.92, "spc": 0.90, "domain": "Tech"},
            {"name": "Project B", "local_score": 1200.0, "pri": 0.75, "caf": 0.70, "spc": 0.65, "domain": "Health"},
            {"name": "Project C", "local_score": 600.0, "pri": 0.50, "caf": 0.45, "spc": 0.40, "domain": "Other"},
        ]
        
        result = self.analyzer.batch_analyze(portfolio)
        
        # Portfolio powinno zawierać projekty do skalowania
        self.assertGreater(result['projects_for_global_scale'], 0)


if __name__ == '__main__':
    # Uruchom testy z verbose output
    unittest.main(verbosity=2)
