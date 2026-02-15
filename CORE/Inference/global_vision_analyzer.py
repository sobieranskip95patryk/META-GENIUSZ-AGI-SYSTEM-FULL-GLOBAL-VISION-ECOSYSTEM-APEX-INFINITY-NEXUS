"""
GlobalVision: Planetary Impact Assessment Engine
================================================

Moduł analityczny do obliczania Global Impact Score (GIS) i oceny wpływu projektów
na skalę planetarną. System wspiera (nie zastępuje) decyzje człowieka.

Autor: META-GENIUSZ® (Patryk Sobierański)
Data: 27 stycznia 2026
Wersja: 1.0 – Pure Analytical Mode
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import json
from datetime import datetime


@dataclass
class PlanetaryImpactMetrics:
    """Metryki wpływu planetarnego projektu."""
    
    local_score: float  # GOK:AI LocalScore (0–2000)
    pri: float          # Planetary Resonance Index (0.0–1.0)
    caf: float          # Civilization Alignment Factor (0.0–1.0)
    spc: float          # Synergy Potential Coefficient (0.0–1.0)
    gis: float          # Global Impact Score (0–10000)
    
    # Metadane
    project_name: str = ""
    creator_name: str = ""
    domain: str = ""
    timestamp: str = ""
    
    def to_dict(self) -> Dict:
        """Konwersja do słownika."""
        return {
            'local_score': round(self.local_score, 2),
            'pri': round(self.pri, 4),
            'caf': round(self.caf, 4),
            'spc': round(self.spc, 4),
            'gis': round(self.gis, 2),
            'project_name': self.project_name,
            'creator_name': self.creator_name,
            'domain': self.domain,
            'timestamp': self.timestamp,
        }


class GlobalVisionAnalyzer:
    """
    Analizator do oceny wpływu projektów na skalę planetarną.
    
    System jest CZYSTO ANALITYCZNY — oblicza metryki, generuje rekomendacje,
    ale nie podejmuje autonomicznych decyzji ani działań.
    """
    
    # Wagi strategiczne (podlegają audytowi i przejrzystości)
    WEIGHT_PRI = 0.40  # Planetary Resonance Index
    WEIGHT_CAF = 0.35  # Civilization Alignment Factor
    WEIGHT_SPC = 0.15  # Synergy Potential Coefficient
    WEIGHT_LS = 0.10   # Local Score (znormalizowany)
    
    # Normalizacja LocalScore
    LOCAL_SCORE_MAX = 2000.0  # Maksymalny potencjał GOK:AI
    
    # Progi decyzyjne (transparentne, audytowalne)
    THRESHOLD_GLOBAL_SCALE = 8500  # GIS do skalowania globalnego
    THRESHOLD_HIGH_POTENTIAL = 6500  # Wysoki potencjał
    THRESHOLD_LOCAL_RELEVANCE = 4000  # Istotność lokalna
    
    def __init__(self):
        """Inicjalizacja analizatora."""
        self.audit_log = []
        self.analysis_history = []
    
    def calculate_gis(
        self,
        local_score: float,
        pri: float,
        caf: float,
        spc: float,
        project_name: str = "Unnamed Project",
        creator_name: str = "Anonymous",
        domain: str = "General",
    ) -> PlanetaryImpactMetrics:
        """
        Oblicza Global Impact Score (GIS) na podstawie wskaźników planetarnych.
        
        Parametry:
        -----------
        local_score : float
            Wynik lokalny z GOK:AI (0–2000)
        pri : float
            Planetary Resonance Index (0.0–1.0)
            Zgodność z wartościami, emocjami, intencjami społecznymi
        caf : float
            Civilization Alignment Factor (0.0–1.0)
            Zgodność z kierunkiem ewolucji cywilizacyjnej
        spc : float
            Synergy Potential Coefficient (0.0–1.0)
            Potencjał synergii między projektami/sektorami
        project_name : str
            Nazwa projektu (dla audytu i raportowania)
        creator_name : str
            Imię/nazwa twórcy
        domain : str
            Domena projektu (edukacja, finanse, ekologia itd.)
        
        Zwraca:
        --------
        PlanetaryImpactMetrics
            Metryki zawierające GIS i wszystkie wskaźniki składowe
        
        Uwagi:
        ------
        - System jest PRZEJRZYSTY: każdy obliczenie jest audytowalne
        - Wszystkie wyniki to REKOMENDACJE, nie autonomiczne decyzje
        - Wzór jest liniowy (unika ukrytych optymizacji)
        """
        
        # Walidacja wejść
        if not (0 <= local_score <= self.LOCAL_SCORE_MAX * 1.5):
            self._log_validation_warning(
                f"LocalScore {local_score} poza typowym zakresem (0–2000)"
            )
        
        if not all(0.0 <= x <= 1.0 for x in [pri, caf, spc]):
            raise ValueError(
                f"PRI, CAF, SPC muszą być w zakresie [0.0, 1.0]. "
                f"Otrzymano: PRI={pri}, CAF={caf}, SPC={spc}"
            )
        
        # Normalizacja LocalScore
        normalized_ls = min(local_score / self.LOCAL_SCORE_MAX, 1.0)
        
        # Obliczenie GIS (wzór przejrzysty, audytowalny)
        gis_normalized = (
            (pri * self.WEIGHT_PRI) +
            (caf * self.WEIGHT_CAF) +
            (spc * self.WEIGHT_SPC) +
            (normalized_ls * self.WEIGHT_LS)
        )
        
        gis = gis_normalized * 10000  # Skalowanie do 0–10000
        
        # Utworzenie metryki
        metrics = PlanetaryImpactMetrics(
            local_score=local_score,
            pri=pri,
            caf=caf,
            spc=spc,
            gis=gis,
            project_name=project_name,
            creator_name=creator_name,
            domain=domain,
            timestamp=datetime.now().isoformat(),
        )
        
        # Rejestracja w historii (dla audytu)
        self._register_analysis(metrics)
        
        return metrics
    
    def get_recommendation(self, metrics: PlanetaryImpactMetrics) -> Dict:
        """
        Generuje rekomendację strategiczną na podstawie GIS i wskaźników.
        
        Parametry:
        -----------
        metrics : PlanetaryImpactMetrics
            Metryki z obliczonego GIS
        
        Zwraca:
        --------
        Dict z rekomendacją zawierającą:
        - recommendation_level: str (GLOBAL_SCALE, HIGH_POTENTIAL, LOCAL_RELEVANCE, REVIEW_NEEDED)
        - gis: float
        - explanation: str
        - action_items: List[str]
        - risk_factors: List[str]
        - synergy_opportunities: List[str]
        
        Uwagi:
        ------
        To są SUGESTIE dla decydentów, nie polecenia do automatycznej egzekucji.
        """
        
        gis = metrics.gis
        
        # Klasyfikacja na podstawie GIS
        if gis >= self.THRESHOLD_GLOBAL_SCALE:
            level = "GLOBAL_SCALE"
            explanation = (
                f"Projekt {metrics.project_name} ma wysoki potencjał do skalowania "
                f"na skalę globalną (GIS: {gis:.2f}). Rekomendacja: integracja z finansowaniem "
                f"ESG, pozycjonowanie w Apex INFINITY, partnerstwa międzynarodowe."
            )
            action_items = [
                "Przygotować dokumentację do funduszy ESG/impact investing",
                "Zdefiniować metryki wpływu dla raportowania SDG",
                "Zidentyfikować 3–5 potencjalnych partnerów międzynarodowych",
                "Opracować narrację planetarną (Apex INFINITY)",
            ]
        
        elif gis >= self.THRESHOLD_HIGH_POTENTIAL:
            level = "HIGH_POTENTIAL"
            explanation = (
                f"Projekt {metrics.project_name} ma wysoki potencjał, ale wymaga "
                f"wzmocnienia w wybranych obszarach (GIS: {gis:.2f}). "
                f"Analiza wskaźników pokazuje obszary do poprawy."
            )
            action_items = [
                "Zidentyfikować obszary słabego PRI/CAF/SPC",
                "Opracować plan wzmocnienia zgodności wartościowej",
                "Poszukać synergii z istniejącymi projektami",
                "Przygotować pilot w wybranym rynku",
            ]
        
        elif gis >= self.THRESHOLD_LOCAL_RELEVANCE:
            level = "LOCAL_RELEVANCE"
            explanation = (
                f"Projekt {metrics.project_name} jest ważny lokalnie, "
                f"ale wymaga znacznego wzmocnienia dla wpływu globalnego (GIS: {gis:.2f})."
            )
            action_items = [
                "Przeprowadzić warsztat wartościowo-celowy z zespołem",
                "Zmapować potencjalnych partnerów w lokalnym ekosystemie",
                "Opracować plan iteracyjnego poprawiania wskaźników",
            ]
        
        else:
            level = "REVIEW_NEEDED"
            explanation = (
                f"Projekt {metrics.project_name} wymaga gruntownej rewizji "
                f"pod kątem zgodności z kierunkami cywilizacyjnymi (GIS: {gis:.2f})."
            )
            action_items = [
                "Przeanalizować niewyrównania PRI/CAF/SPC",
                "Przeprowadzić sesję projektowania wartościowego",
                "Rozważyć zmianę podejścia lub zakresu projektu",
            ]
        
        # Analiza ryzyka (oparta na wskaźnikach)
        risk_factors = []
        if metrics.pri < 0.7:
            risk_factors.append(
                f"Niski rezonans wartościowy (PRI: {metrics.pri:.2f}) — "
                f"projekt może nie rezonować z emocjami i intencjami społecznymi"
            )
        if metrics.caf < 0.7:
            risk_factors.append(
                f"Niedostateczna zgodność cywilizacyjna (CAF: {metrics.caf:.2f}) — "
                f"projekt może być niezgodny z kierunkiem ewolucji"
            )
        if metrics.spc < 0.6:
            risk_factors.append(
                f"Niski potencjał synergii (SPC: {metrics.spc:.2f}) — "
                f"projekt działa w silosie, bez ekosystemu"
            )
        if metrics.local_score < 800:
            risk_factors.append(
                f"Niski potencjał lokalny (LS: {metrics.local_score:.2f}) — "
                f"podstawa do skalowania jest słaba"
            )
        
        # Okazje synergii
        synergy_opportunities = []
        if metrics.caf > 0.85 and metrics.spc > 0.75:
            synergy_opportunities.append(
                "Wysoki potencjał do powiązania z inicjatywami klimatycznymi/SDG"
            )
        if metrics.pri > 0.8 and metrics.local_score > 1500:
            synergy_opportunities.append(
                "Potencjał do zostania 'Rezonatorem Planetarnym' — ikona w Apex INFINITY"
            )
        if metrics.spc > 0.8:
            synergy_opportunities.append(
                "Możliwość tworzenia platformy / ekosystemu współpracy"
            )
        
        return {
            "recommendation_level": level,
            "gis": round(metrics.gis, 2),
            "explanation": explanation,
            "action_items": action_items,
            "risk_factors": risk_factors if risk_factors else ["Brak znaczących ryzyk"],
            "synergy_opportunities": synergy_opportunities if synergy_opportunities else ["Możliwe są synergii po wzmocnieniu wskaźników"],
            "timestamp": datetime.now().isoformat(),
            "disclaimer": "To są rekomendacje analityczne. Wszystkie decyzje pozostają pod kontrolą człowieka.",
        }
    
    def batch_analyze(self, projects: list) -> Dict:
        """
        Analiza zbioru projektów i identyfikacja synergii.
        
        Parametry:
        -----------
        projects : List[Dict]
            Lista słowników z danymi projektów:
            {
                'name': str,
                'local_score': float,
                'pri': float,
                'caf': float,
                'spc': float,
                'domain': str,
            }
        
        Zwraca:
        --------
        Dict zawierający analizę całego portfolio'a
        """
        
        if not projects:
            raise ValueError("Lista projektów nie może być pusta")
        
        analyses = []
        for project in projects:
            metrics = self.calculate_gis(
                local_score=project.get('local_score', 1000),
                pri=project.get('pri', 0.5),
                caf=project.get('caf', 0.5),
                spc=project.get('spc', 0.5),
                project_name=project.get('name', 'Unknown'),
                domain=project.get('domain', 'General'),
            )
            analyses.append(metrics.to_dict())
        
        # Statystyki portfolio
        gis_values = [a['gis'] for a in analyses]
        avg_gis = sum(gis_values) / len(gis_values)
        max_gis = max(gis_values)
        min_gis = min(gis_values)
        
        # Projekty do skalowania
        global_scale = [a for a in analyses if a['gis'] >= self.THRESHOLD_GLOBAL_SCALE]
        
        return {
            "portfolio_size": len(analyses),
            "average_gis": round(avg_gis, 2),
            "max_gis": round(max_gis, 2),
            "min_gis": round(min_gis, 2),
            "projects_for_global_scale": len(global_scale),
            "all_analyses": analyses,
            "projects_recommended_for_scaling": [p['project_name'] for p in global_scale],
            "timestamp": datetime.now().isoformat(),
        }
    
    def _log_validation_warning(self, message: str):
        """Rejestruj ostrzeżenie walidacji."""
        self.audit_log.append({
            "type": "WARNING",
            "message": message,
            "timestamp": datetime.now().isoformat(),
        })
    
    def _register_analysis(self, metrics: PlanetaryImpactMetrics):
        """Rejestruj analizę w historii (dla audytu)."""
        self.analysis_history.append(metrics.to_dict())
    
    def export_audit_log(self, filepath: str = "gv_audit_log.json"):
        """Eksportuj log audytu do pliku JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(
                {
                    "audit_log": self.audit_log,
                    "analysis_history": self.analysis_history,
                    "export_timestamp": datetime.now().isoformat(),
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
        return filepath


# ============================================================================
# DEMO I TESTY
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("GlobalVision: Planetary Impact Assessment Engine – DEMO")
    print("=" * 80)
    print()
    
    analyzer = GlobalVisionAnalyzer()
    
    # Test 1: Edukacja kosmiczna
    print("📊 Test 1: Projekt Edukacji Kosmicznej")
    print("-" * 80)
    metrics1 = analyzer.calculate_gis(
        local_score=1751.45,
        pri=0.92,
        caf=0.88,
        spc=0.75,
        project_name="Cosmic Education Platform",
        creator_name="Alice Smith",
        domain="Education",
    )
    print(json.dumps(metrics1.to_dict(), indent=2, ensure_ascii=False))
    print()
    
    rec1 = analyzer.get_recommendation(metrics1)
    print("Rekomendacja:")
    print(json.dumps(rec1, indent=2, ensure_ascii=False))
    print()
    print()
    
    # Test 2: Bioenergia
    print("📊 Test 2: Projekt Bioenergii")
    print("-" * 80)
    metrics2 = analyzer.calculate_gis(
        local_score=1240.30,
        pri=0.85,
        caf=0.92,
        spc=0.88,
        project_name="Bioenenergy Microgrids",
        creator_name="Bob Johnson",
        domain="Ecology",
    )
    print(json.dumps(metrics2.to_dict(), indent=2, ensure_ascii=False))
    print()
    
    rec2 = analyzer.get_recommendation(metrics2)
    print("Rekomendacja:")
    print(json.dumps(rec2, indent=2, ensure_ascii=False))
    print()
    print()
    
    # Test 3: Portfolio analysis
    print("📊 Test 3: Analiza Portfolio (5 projektów)")
    print("-" * 80)
    portfolio = [
        {"name": "Cosmic Education", "local_score": 1751.45, "pri": 0.92, "caf": 0.88, "spc": 0.75, "domain": "Education"},
        {"name": "Bioenenergy", "local_score": 1240.30, "pri": 0.85, "caf": 0.92, "spc": 0.88, "domain": "Ecology"},
        {"name": "Cultural Resonance", "local_score": 980.50, "pri": 0.88, "caf": 0.72, "spc": 0.65, "domain": "Culture"},
        {"name": "FinTech for Good", "local_score": 1500.20, "pri": 0.75, "caf": 0.80, "spc": 0.70, "domain": "Finance"},
        {"name": "Health Tech Startup", "local_score": 1100.00, "pri": 0.70, "caf": 0.65, "spc": 0.60, "domain": "Health"},
    ]
    
    portfolio_analysis = analyzer.batch_analyze(portfolio)
    print(json.dumps(portfolio_analysis, indent=2, ensure_ascii=False))
    print()
    
    # Test 4: Eksport audytu
    print("📋 Test 4: Eksport Log Audytu")
    print("-" * 80)
    audit_file = analyzer.export_audit_log("gv_audit_demo.json")
    print(f"✅ Log audytu eksportowany do: {audit_file}")
    print()
    
    print("=" * 80)
    print("Demo ukończone. System jest czysto ANALITYCZNY — brak autonomicznych decyzji.")
    print("=" * 80)
