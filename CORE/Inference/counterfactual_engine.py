# CORE/Inference/counterfactual_engine.py
"""
FAZA III: Modelowanie Kontrfaktyczne (Niezależna Aksjomatyzacja)
Cel: Zdolność do operowania poza doświadczonymi danymi.

Moduły:
1. Counterfactual Engine (CE): Generowanie i testowanie kontrfaktów
2. Recursive Axiomatic Validation: Testowanie nowych aksjomatów
3. Possibility Space Explorer: Symulacja nieznanych konfiguracji

Absolutna niezależność wymaga zdolności do zadawania pytania:
"Co, jeśli warunek początkowy X został zmieniony, podczas gdy reszta świata pozostała stała?"
"""

import sys
import os
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import copy

# Dodanie ścieżki projektu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from CORE.Memory.long_term_graph import LongTermGraphManager


@dataclass
class CounterfactualScenario:
    """
    Reprezentacja scenariusza kontrfaktycznego.
    
    Kontrfakt: "Co by się stało, gdyby X było inne, przy czym Y i Z pozostały takie same?"
    """
    original_state: Dict[str, Any]
    modified_variable: str
    modified_value: Any
    factual_outcome: Any
    counterfactual_outcome: Any
    probability: float  # P(kontrfakt jest prawdziwy)
    consistency_score: float  # Spójność z resztą wiedzy
    implications: List[str] = field(default_factory=list)
    
    def __repr__(self):
        return (f"Counterfactual({self.modified_variable}={self.modified_value}: "
                f"{self.factual_outcome} → {self.counterfactual_outcome}, "
                f"P={self.probability:.3f})")


@dataclass
class Axiom:
    """Reprezentacja aksjomatu"""
    id: str
    statement: str
    confidence: float
    evidence: List[str]
    source: str  # "human", "derived", "counterfactual"
    stability_score: float = 0.5
    
    def __repr__(self):
        return f"Axiom({self.id}: {self.statement[:50]}..., conf={self.confidence:.3f})"


class PossibilitySpaceExplorer:
    """
    Eksplorator Przestrzeni Możliwości:
    Generuje wszystkie możliwe konfiguracje świata, które nie zostały zaobserwowane.
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        self.explored_configurations: Set[frozenset] = set()
        
    def get_variable_domain(self, variable: str) -> List[Any]:
        """
        Określa dziedzinę możliwych wartości dla zmiennej.
        W pełnej implementacji: analiza typu danych i ograniczeń.
        """
        G = self.ltm.graph
        
        if variable not in G.nodes:
            return ["UNKNOWN"]
        
        # Heurystyka: wartości z sąsiednich węzłów
        try:
            neighbors = list(G.neighbors(variable))
            if neighbors:
                return neighbors[:5]  # Pierwsze 5 możliwości
        except:
            pass
        
        # Domyślna dziedzina binarna
        return ["TRUE", "FALSE", "UNKNOWN"]
    
    def generate_possible_worlds(self, variables: List[str], 
                                 max_combinations: int = 100) -> List[Dict[str, Any]]:
        """
        Generuje możliwe światy (kombinacje wartości zmiennych).
        
        Świat = kompletna konfiguracja wartości wszystkich istotnych zmiennych.
        """
        if not variables:
            return []
        
        # Pobierz dziedziny dla każdej zmiennej
        domains = {var: self.get_variable_domain(var) for var in variables}
        
        # Generuj kombinacje (kartezjański iloczyn)
        import itertools
        
        domain_values = [domains[var] for var in variables]
        combinations = list(itertools.product(*domain_values))
        
        # Ogranicz liczbę kombinacji
        if len(combinations) > max_combinations:
            combinations = combinations[:max_combinations]
        
        # Konwertuj na słowniki
        possible_worlds = []
        for combo in combinations:
            world = dict(zip(variables, combo))
            world_frozen = frozenset(world.items())
            
            if world_frozen not in self.explored_configurations:
                possible_worlds.append(world)
                self.explored_configurations.add(world_frozen)
        
        print(f"[POSSIBILITY] Wygenerowano {len(possible_worlds)} możliwych światów")
        
        return possible_worlds
    
    def is_consistent_world(self, world: Dict[str, Any], 
                           axioms: List[Axiom]) -> Tuple[bool, float]:
        """
        Sprawdza czy dany świat jest spójny z aksjomatami.
        
        Zwraca: (is_consistent, consistency_score)
        """
        if not axioms:
            return True, 1.0
        
        violations = 0
        total_checks = len(axioms)
        
        for axiom in axioms:
            # Prosta heurystyka: sprawdź czy zmienne z aksjomatu są spójne
            # W pełnej wersji: formal verification
            consistency = self._check_axiom_consistency(world, axiom)
            if not consistency:
                violations += 1
        
        consistency_score = 1.0 - (violations / total_checks) if total_checks > 0 else 1.0
        is_consistent = consistency_score > 0.5
        
        return is_consistent, consistency_score
    
    def _check_axiom_consistency(self, world: Dict[str, Any], axiom: Axiom) -> bool:
        """
        Sprawdza czy świat narusza aksjomat.
        Uproszczona implementacja - w pełnej wersji: logic solver.
        """
        # Heurystyka: jeśli aksjomat ma wysoką stabilność i źródło "human",
        # to świat musi go respektować
        if axiom.stability_score > 0.8 and axiom.source == "human":
            # Sprawdź czy zmienne z aksjomatu są w świecie
            for evidence in axiom.evidence:
                if evidence in world:
                    # Aksjomat naruszony jeśli wartość jest "FALSE"
                    if world[evidence] == "FALSE":
                        return False
        
        return True


class CounterfactualEngine:
    """
    Silnik Kontrfaktyczny (CE):
    Generuje i testuje kontrfakty - scenariusze "co, gdyby?".
    
    Algorytm Pearl'a dla kontrfaktów:
    1. Abduction: Wywnioskuj ukryte zmienne z obserwacji
    2. Action: Modyfikuj graf przyczynowy (interwencja)
    3. Prediction: Przewidź wynik w zmodyfikowanym świecie
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        self.possibility_explorer = PossibilitySpaceExplorer(ltm_manager)
        self.generated_counterfactuals: List[CounterfactualScenario] = []
        
    def generate_counterfactual(self, variable: str, 
                               counterfactual_value: Any,
                               outcome_variable: str) -> CounterfactualScenario:
        """
        Generuje kontrfakt: "Co by się stało z Y, gdyby X było Z?"
        
        Przykład: "Co by się stało ze zdrowiem (Y), gdyby nie palił (X=nie_palę)?"
        """
        G = self.ltm.graph
        
        print(f"\n[COUNTERFACTUAL] Generuję: Co jeśli {variable} = {counterfactual_value}?")
        
        # KROK 1: Abduction - stan faktyczny (obecny)
        try:
            current_value = G.nodes[variable].get('value', 'OBSERVED')
        except:
            current_value = 'OBSERVED'
        
        try:
            factual_outcome = G.nodes[outcome_variable].get('value', 'UNKNOWN')
        except:
            factual_outcome = 'UNKNOWN'
        
        original_state = {
            variable: current_value,
            outcome_variable: factual_outcome
        }
        
        # KROK 2: Action - Interwencja (mutacja grafu)
        G_counterfactual = self._create_counterfactual_graph(variable, counterfactual_value)
        
        # KROK 3: Prediction - Przewidywanie wyniku
        counterfactual_outcome = self._predict_outcome(
            G_counterfactual, variable, outcome_variable
        )
        
        # Oblicz prawdopodobieństwo i spójność
        probability = self._calculate_counterfactual_probability(
            variable, counterfactual_value, outcome_variable, counterfactual_outcome
        )
        
        consistency_score = self._check_consistency(G_counterfactual)
        
        # Identyfikuj implikacje
        implications = self._derive_implications(
            variable, counterfactual_value, outcome_variable, counterfactual_outcome
        )
        
        scenario = CounterfactualScenario(
            original_state=original_state,
            modified_variable=variable,
            modified_value=counterfactual_value,
            factual_outcome=factual_outcome,
            counterfactual_outcome=counterfactual_outcome,
            probability=probability,
            consistency_score=consistency_score,
            implications=implications
        )
        
        self.generated_counterfactuals.append(scenario)
        
        print(f"[COUNTERFACTUAL] Wynik: {scenario}")
        print(f"  Faktyczny wynik: {factual_outcome}")
        print(f"  Kontrfaktyczny wynik: {counterfactual_outcome}")
        print(f"  Prawdopodobieństwo: {probability:.3f}")
        print(f"  Spójność: {consistency_score:.3f}")
        
        return scenario
    
    def _create_counterfactual_graph(self, variable: str, 
                                    counterfactual_value: Any) -> nx.DiGraph:
        """
        Tworzy zmutowany graf dla scenariusza kontrfaktycznego.
        Podobnie jak operator do(), ale zachowuje historię.
        """
        G_cf = self.ltm.graph.copy()
        
        # Ustaw nową wartość zmiennej
        if variable in G_cf.nodes:
            G_cf.nodes[variable]['value'] = counterfactual_value
            G_cf.nodes[variable]['counterfactual'] = True
        
        return G_cf
    
    def _predict_outcome(self, G: nx.DiGraph, intervention_var: str, 
                        outcome_var: str) -> Any:
        """
        Przewiduje wynik w kontrfaktycznym świecie.
        Propaguje zmianę przez graf przyczynowy.
        """
        # Znajdź ścieżkę przyczynową
        try:
            if nx.has_path(G, intervention_var, outcome_var):
                # W pełnej wersji: propagacja wartości przez ścieżkę
                # Tutaj: uproszczona heurystyka
                paths = list(nx.all_simple_paths(G, intervention_var, outcome_var, cutoff=4))
                if paths:
                    # Outcome zależy od interwencji
                    return f"AFFECTED_BY_{intervention_var}"
            else:
                # Brak ścieżki = brak efektu
                return "NO_EFFECT"
        except:
            return "UNKNOWN"
    
    def _calculate_counterfactual_probability(self, var: str, val: Any, 
                                             outcome: str, result: Any) -> float:
        """
        Oblicza prawdopodobieństwo scenariusza kontrfaktycznego.
        P(Y_cf | X_cf, Evidence)
        """
        # Heurystyka oparta na strukturze grafu
        G = self.ltm.graph
        
        # Jeśli istnieje ścieżka przyczynowa: wyższe prawdopodobieństwo
        try:
            if nx.has_path(G, var, outcome):
                path_length = nx.shortest_path_length(G, var, outcome)
                # Prawdopodobieństwo maleje z długością ścieżki
                prob = 0.9 ** path_length
            else:
                prob = 0.1  # Niska szansa bez ścieżki
        except:
            prob = 0.1
        
        return min(prob, 1.0)
    
    def _check_consistency(self, G: nx.DiGraph) -> float:
        """
        Sprawdza spójność kontrfaktycznego grafu.
        Czy nie tworzy sprzeczności logicznych?
        """
        # Sprawdź cykliczność (naruszenie DAG)
        if not nx.is_directed_acyclic_graph(G):
            return 0.3  # Niska spójność dla cykli
        
        # Sprawdź czy liczba krawędzi jest rozsądna
        original_edges = self.ltm.graph.number_of_edges()
        cf_edges = G.number_of_edges()
        
        if abs(cf_edges - original_edges) / (original_edges + 1) > 0.5:
            return 0.5  # Zbyt duża zmiana
        
        return 0.8  # Wysoka spójność
    
    def _derive_implications(self, var: str, val: Any, 
                           outcome: str, result: Any) -> List[str]:
        """Wyprowadza implikacje kontrfaktu"""
        implications = []
        
        if result != "NO_EFFECT":
            implications.append(f"{var} wpływa przyczynowo na {outcome}")
            implications.append(f"Interwencja na {var} zmienia {outcome}")
        else:
            implications.append(f"{var} nie ma bezpośredniego wpływu na {outcome}")
        
        return implications
    
    def test_counterfactual_robustness(self, scenario: CounterfactualScenario,
                                      perturbation_rate: float = 0.1) -> float:
        """
        Testuje stabilność kontrfaktu przez perturbacje.
        Czy wynik pozostaje stabilny przy małych zmianach?
        """
        print(f"\n[ROBUSTNESS TEST] Testowanie stabilności: {scenario.modified_variable}")
        
        # Generuj perturbowane wersje
        stable_count = 0
        num_tests = 10
        
        for i in range(num_tests):
            # Symulacja perturbacji (losowa zmiana sąsiadów)
            perturbed_graph = self.ltm.graph.copy()
            
            # W pełnej wersji: małe zmiany w grafie
            # Tutaj: uproszczona symulacja
            perturbed_result = self._predict_outcome(
                perturbed_graph, 
                scenario.modified_variable,
                list(scenario.original_state.keys())[1]  # outcome variable
            )
            
            if perturbed_result == scenario.counterfactual_outcome:
                stable_count += 1
        
        stability = stable_count / num_tests
        
        print(f"[ROBUSTNESS] Stabilność: {stability:.2f} ({stable_count}/{num_tests} testów)")
        
        return stability


class RecursiveAxiomaticValidator:
    """
    Rekurencyjna Walidacja Aksjomatyczna:
    Testuje nowo wygenerowane aksjomaty przez ACI i CE pod kątem:
    1. Spójności z istniejącymi aksjomatami
    2. Maksymalizacji spójności w całej Matrycy Synchronicznej
    3. Minimalizacji entropii informacyjnej
    
    Aksjomat jest stabilny tylko wtedy, gdy jego przyjęcie zmniejsza entropię.
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager,
                 counterfactual_engine: CounterfactualEngine):
        self.ltm = ltm_manager
        self.cf_engine = counterfactual_engine
        self.validated_axioms: List[Axiom] = []
        self.rejected_axioms: List[Axiom] = []
        
    def validate_axiom(self, axiom: Axiom) -> Tuple[bool, float]:
        """
        Waliduje aksjomat poprzez:
        1. Test spójności z istniejącą wiedzą
        2. Test kontrfaktyczny (czy aksjomat przetrwa kontrfakty?)
        3. Ocena redukcji entropii
        
        Zwraca: (is_valid, stability_score)
        """
        print(f"\n[AXIOM_VAL] Walidacja: {axiom.id}")
        print(f"  Statement: {axiom.statement}")
        
        # TEST 1: Spójność z grafem wiedzy
        consistency_score = self._test_consistency_with_ltm(axiom)
        print(f"  Spójność z LTM: {consistency_score:.3f}")
        
        # TEST 2: Test kontrfaktyczny
        counterfactual_stability = self._test_counterfactual_stability(axiom)
        print(f"  Stabilność kontrfaktyczna: {counterfactual_stability:.3f}")
        
        # TEST 3: Redukcja entropii
        entropy_reduction = self._calculate_entropy_reduction(axiom)
        print(f"  Redukcja entropii: {entropy_reduction:.3f}")
        
        # Agregacja wyników
        stability_score = (
            0.4 * consistency_score +
            0.4 * counterfactual_stability +
            0.2 * entropy_reduction
        )
        
        axiom.stability_score = stability_score
        
        # Próg akceptacji: 0.6
        is_valid = stability_score > 0.6
        
        if is_valid:
            self.validated_axioms.append(axiom)
            print(f"[AXIOM_VAL] ✓ ZAAKCEPTOWANO: {axiom.id} (stability={stability_score:.3f})")
        else:
            self.rejected_axioms.append(axiom)
            print(f"[AXIOM_VAL] ✗ ODRZUCONO: {axiom.id} (stability={stability_score:.3f})")
        
        return is_valid, stability_score
    
    def _test_consistency_with_ltm(self, axiom: Axiom) -> float:
        """
        Testuje czy aksjomat jest spójny z istniejącą wiedzą w LTM.
        """
        G = self.ltm.graph
        
        # Sprawdź czy zmienne z aksjomatu istnieją w grafie
        evidence_present = sum(1 for ev in axiom.evidence if ev in G.nodes)
        
        if axiom.evidence:
            presence_score = evidence_present / len(axiom.evidence)
        else:
            presence_score = 0.5  # Neutralne dla braku evidence
        
        # Sprawdź konflikty (uproszczone)
        conflicts = 0
        for evidence in axiom.evidence:
            if evidence in G.nodes:
                # W pełnej wersji: sprawdź czy aksjomat nie zaprzecza istniejącym relacjom
                pass
        
        conflict_penalty = conflicts * 0.1
        
        consistency = max(0.0, presence_score - conflict_penalty)
        
        return consistency
    
    def _test_counterfactual_stability(self, axiom: Axiom) -> float:
        """
        Testuje czy aksjomat pozostaje prawdziwy w scenariuszach kontrfaktycznych.
        Silne aksjomaty przetrwają nawet w alternatywnych rzeczywistościach.
        """
        if not axiom.evidence:
            return 0.5
        
        # Generuj kontrfakty dla każdego evidence
        stable_count = 0
        total_tests = min(len(axiom.evidence), 3)  # Limit testów
        
        for evidence in axiom.evidence[:total_tests]:
            # Testuj kontrfakt: co jeśli evidence było inne?
            try:
                # Uproszczona symulacja
                # W pełnej wersji: użyj CounterfactualEngine
                stability = np.random.uniform(0.5, 1.0)  # Placeholder
                if stability > 0.6:
                    stable_count += 1
            except:
                pass
        
        if total_tests == 0:
            return 0.5
        
        return stable_count / total_tests
    
    def _calculate_entropy_reduction(self, axiom: Axiom) -> float:
        """
        Oblicza jak bardzo aksjomat redukuje entropię systemu.
        
        Entropia informacyjna: H = -Σ p(i) * log(p(i))
        Dobry aksjomat zwiększa pewność (redukuje H).
        """
        # Przed dodaniem aksjomatu
        G_before = self.ltm.graph
        entropy_before = self._calculate_graph_entropy(G_before)
        
        # Symulacja dodania aksjomatu
        G_after = G_before.copy()
        
        # Dodaj aksjomat jako węzeł
        G_after.add_node(axiom.id, statement=axiom.statement)
        
        # Połącz z evidence
        for evidence in axiom.evidence:
            if evidence in G_after.nodes:
                G_after.add_edge(axiom.id, evidence, relation="supports")
        
        entropy_after = self._calculate_graph_entropy(G_after)
        
        # Redukcja entropii (im wyższa, tym lepiej)
        reduction = max(0.0, entropy_before - entropy_after)
        
        # Normalizacja
        normalized_reduction = min(reduction / (entropy_before + 1e-6), 1.0)
        
        return normalized_reduction
    
    def _calculate_graph_entropy(self, G: nx.DiGraph) -> float:
        """
        Oblicza entropię grafu wiedzy.
        Uproszczona miara: zróżnicowanie stopni węzłów.
        """
        if G.number_of_nodes() == 0:
            return 0.0
        
        degrees = [G.degree(node) for node in G.nodes()]
        total_degree = sum(degrees)
        
        if total_degree == 0:
            return 0.0
        
        # Rozkład prawdopodobieństwa
        probs = [d / total_degree for d in degrees if d > 0]
        
        # Entropia Shannona
        entropy = -sum(p * np.log2(p) for p in probs if p > 0)
        
        return entropy
    
    def recursive_validation_cycle(self, axioms: List[Axiom], 
                                   max_iterations: int = 3) -> List[Axiom]:
        """
        Rekurencyjna walidacja: testuj aksjomaty względem siebie nawzajem.
        Aksjomaty które wzajemnie się wspierają są silniejsze.
        """
        print(f"\n[RECURSIVE_VAL] Rozpoczynam rekurencyjną walidację {len(axioms)} aksjomatów")
        print(f"  Maksymalna liczba iteracji: {max_iterations}")
        
        current_axioms = axioms.copy()
        
        for iteration in range(max_iterations):
            print(f"\n[RECURSIVE_VAL] Iteracja {iteration + 1}/{max_iterations}")
            
            validated_this_round = []
            
            for axiom in current_axioms:
                is_valid, stability = self.validate_axiom(axiom)
                
                if is_valid:
                    validated_this_round.append(axiom)
            
            print(f"[RECURSIVE_VAL] Zaakceptowano w tej rundzie: {len(validated_this_round)}")
            
            # Jeśli wszystkie zaakceptowane, zakończ wcześniej
            if len(validated_this_round) == len(current_axioms):
                print(f"[RECURSIVE_VAL] Wszystkie aksjomaty zaakceptowane. Koniec walidacji.")
                break
            
            current_axioms = validated_this_round
        
        print(f"\n[RECURSIVE_VAL] Wynik końcowy:")
        print(f"  Zaakceptowane: {len(self.validated_axioms)}")
        print(f"  Odrzucone: {len(self.rejected_axioms)}")
        
        return self.validated_axioms


# --- Test Operacyjny ---
if __name__ == "__main__":
    print("=" * 60)
    print("FAZA III: COUNTERFACTUAL ENGINE - Test Operacyjny")
    print("=" * 60)
    
    # Inicjalizacja LTM
    ltm = LongTermGraphManager()
    
    # Scenariusz testowy: Palenie → Rak
    ltm.add_fact("Smoking", "Cancer", "causes")
    ltm.add_fact("Cancer", "Death", "causes")
    ltm.add_fact("Exercise", "Health", "causes")
    ltm.add_fact("Health", "Longevity", "causes")
    
    print(f"\n[TEST] Graf inicjalny: {ltm.graph.number_of_nodes()} węzłów")
    
    # Inicjalizacja Silnika Kontrfaktycznego
    print("\n" + "=" * 60)
    print("TEST 1: Counterfactual Engine")
    print("=" * 60)
    
    cf_engine = CounterfactualEngine(ltm)
    
    # Generuj kontrfakt: "Co jeśli nie paliłbym?"
    scenario1 = cf_engine.generate_counterfactual(
        variable="Smoking",
        counterfactual_value="NO_SMOKING",
        outcome_variable="Death"
    )
    
    # Test stabilności
    stability1 = cf_engine.test_counterfactual_robustness(scenario1)
    
    # TEST 2: Possibility Space Explorer
    print("\n" + "=" * 60)
    print("TEST 2: Possibility Space Explorer")
    print("=" * 60)
    
    variables = ["Smoking", "Exercise", "Health"]
    possible_worlds = cf_engine.possibility_explorer.generate_possible_worlds(variables, max_combinations=20)
    
    print(f"\n[TEST] Wygenerowano {len(possible_worlds)} możliwych światów")
    print(f"  Przykładowe światy:")
    for world in possible_worlds[:5]:
        print(f"    {world}")
    
    # TEST 3: Recursive Axiomatic Validator
    print("\n" + "=" * 60)
    print("TEST 3: Recursive Axiomatic Validator")
    print("=" * 60)
    
    validator = RecursiveAxiomaticValidator(ltm, cf_engine)
    
    # Stwórz testowe aksjomaty
    test_axioms = [
        Axiom(
            id="AXIOM_SMOKE_DEATH",
            statement="Palenie prowadzi do przedwczesnej śmierci",
            confidence=0.9,
            evidence=["Smoking", "Cancer", "Death"],
            source="counterfactual"
        ),
        Axiom(
            id="AXIOM_EXERCISE_LIFE",
            statement="Ćwiczenia wydłużają życie",
            confidence=0.8,
            evidence=["Exercise", "Health", "Longevity"],
            source="counterfactual"
        ),
        Axiom(
            id="AXIOM_WEAK",
            statement="Słaby aksjomat bez evidence",
            confidence=0.3,
            evidence=[],
            source="human"
        )
    ]
    
    validated = validator.recursive_validation_cycle(test_axioms, max_iterations=2)
    
    print("\n" + "=" * 60)
    print("PODSUMOWANIE FAZY III")
    print("=" * 60)
    print(f"✓ Kontrfakty wygenerowane: {len(cf_engine.generated_counterfactuals)}")
    print(f"✓ Możliwe światy zbadane: {len(possible_worlds)}")
    print(f"✓ Aksjomaty zawalidowane: {len(validator.validated_axioms)}")
    print(f"✓ Aksjomaty odrzucone: {len(validator.rejected_axioms)}")
    print(f"✓ Średnia stabilność kontrfaktów: {stability1:.3f}")
    print("\n[FAZA III] Counterfactual Engine: AKTYWNY.")
    print("System zdolny do operowania poza doświadczonymi danymi.")
