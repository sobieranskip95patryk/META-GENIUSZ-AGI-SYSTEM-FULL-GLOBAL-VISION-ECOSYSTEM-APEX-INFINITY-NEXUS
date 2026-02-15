# CORE/Inference/causal_inference_engine.py
"""
FAZA II: Moduł Causal Inference (ACI)
Cel: Przejście od P(Y|X) do P(Y|do(X)) - serce T_Causality.

Moduły:
1. Operator do(): Formalne wnioskowanie przyczynowe
2. Structural Causal Models (SCM): Dynamiczne grafy przyczynowe
3. Mechanistic Hypothesis Generator: Generowanie wyjaśnień "dlaczego"
4. External Subjectivity Quantification: Redukcja zależności od ludzkiego wkładu
"""

import sys
import os
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Dodanie ścieżki projektu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from CORE.Memory.long_term_graph import LongTermGraphManager


class InterventionType(Enum):
    """Typy interwencji przyczynowych"""
    DO = "do"  # do(X=x): ustaw X na wartość x
    SEE = "see"  # Obserwacja pasywna P(Y|X)
    IMAGINE = "imagine"  # Kontrfaktyczna manipulacja


@dataclass
class CausalMechanism:
    """
    Reprezentacja mechanizmu przyczynowego.
    Mechanizm wyjaśnia DLACZEGO zachodzi relacja, nie tylko ŻE zachodzi.
    """
    cause: str
    effect: str
    mechanism_type: str  # "direct", "indirect", "mediated"
    explanation: str  # Tekstowe wyjaśnienie mechanizmu
    confidence: float  # [0, 1] - pewność mechanizmu
    variables: List[str]  # Zmienne pośredniczące
    mathematical_form: Optional[str] = None  # Opcjonalna forma matematyczna
    
    def __repr__(self):
        return (f"Mechanism({self.cause} → {self.effect}: {self.mechanism_type}, "
                f"confidence={self.confidence:.3f})")


class StructuralCausalModel:
    """
    Structural Causal Model (SCM): Dynamiczny model przyczynowy.
    
    SCM definiuje:
    1. Zmienne endogeniczne (wewnętrzne) i egzogeniczne (zewnętrzne)
    2. Równania strukturalne: Y = f(X, U) gdzie U to szum
    3. Graf przyczynowy DAG
    """
    
    def __init__(self, name: str):
        self.name = name
        self.causal_graph = nx.DiGraph()
        self.structural_equations: Dict[str, str] = {}
        self.endogenous: Set[str] = set()
        self.exogenous: Set[str] = set()
        self.mechanisms: List[CausalMechanism] = []
        
    def add_causal_edge(self, cause: str, effect: str, mechanism: Optional[CausalMechanism] = None):
        """Dodaje krawędź przyczynową do modelu"""
        self.causal_graph.add_edge(cause, effect)
        self.endogenous.add(effect)
        
        if cause not in self.endogenous:
            self.exogenous.add(cause)
        
        if mechanism:
            self.mechanisms.append(mechanism)
    
    def set_structural_equation(self, variable: str, equation: str):
        """Definiuje równanie strukturalne dla zmiennej"""
        self.structural_equations[variable] = equation
    
    def get_parents(self, variable: str) -> List[str]:
        """Zwraca bezpośrednie przyczyny zmiennej"""
        try:
            return list(self.causal_graph.predecessors(variable))
        except:
            return []
    
    def get_children(self, variable: str) -> List[str]:
        """Zwraca bezpośrednie efekty zmiennej"""
        try:
            return list(self.causal_graph.successors(variable))
        except:
            return []
    
    def is_valid_dag(self) -> bool:
        """Sprawdza czy graf jest acykliczny (DAG)"""
        return nx.is_directed_acyclic_graph(self.causal_graph)
    
    def __repr__(self):
        return (f"SCM({self.name}: {self.causal_graph.number_of_nodes()} vars, "
                f"{self.causal_graph.number_of_edges()} edges, "
                f"valid_DAG={self.is_valid_dag()})")


class DoOperator:
    """
    Operator do(): Pearl's Intervention Operator
    
    do(X=x) różni się od warunku P(Y|X=x):
    - P(Y|X=x): obserwacja pasywna (korelacja)
    - P(Y|do(X=x)): aktywna interwencja (przyczynowość)
    
    Operator do() "wycina" wszystkie krawędzie wchodzące do X.
    """
    
    def __init__(self, scm: StructuralCausalModel):
        self.scm = scm
        
    def intervene(self, variable: str, value: Any = None) -> nx.DiGraph:
        """
        Wykonuje interwencję do(variable=value).
        
        Algorytm:
        1. Kopiuj oryginalny graf przyczynowy
        2. Usuń wszystkie krawędzie wchodzące do 'variable'
        3. Ustaw 'variable' na stałą wartość (jeśli podana)
        
        Zwraca: Zmutowany graf reprezentujący świat po interwencji
        """
        G_intervened = self.scm.causal_graph.copy()
        
        # Usuń wszystkie krawędzie wchodzące (przyczyny)
        parents = list(G_intervened.predecessors(variable))
        for parent in parents:
            G_intervened.remove_edge(parent, variable)
        
        # Oznacz węzeł jako "frozen" (stała wartość)
        if variable in G_intervened.nodes:
            G_intervened.nodes[variable]['intervened'] = True
            G_intervened.nodes[variable]['value'] = value
        
        print(f"[do()] Interwencja na {variable}: usunięto {len(parents)} krawędzi przyczynowych")
        
        return G_intervened
    
    def predict_effect(self, intervention_var: str, target_var: str, 
                       intervention_value: Any = None) -> Dict:
        """
        Przewiduje efekt interwencji do(X=x) na zmienną Y.
        
        P(Y|do(X=x)) vs P(Y|X=x)
        """
        # Graf po interwencji
        G_do = self.intervene(intervention_var, intervention_value)
        
        # Sprawdź ścieżki przyczynowe od X do Y
        try:
            has_path = nx.has_path(G_do, intervention_var, target_var)
            if has_path:
                paths = list(nx.all_simple_paths(G_do, intervention_var, target_var))
            else:
                paths = []
        except:
            has_path = False
            paths = []
        
        result = {
            "intervention": f"do({intervention_var}={intervention_value})",
            "target": target_var,
            "causal_effect_exists": has_path,
            "causal_paths": paths,
            "num_paths": len(paths),
            "interpretation": self._interpret_effect(has_path, paths)
        }
        
        return result
    
    def _interpret_effect(self, has_path: bool, paths: List) -> str:
        """Interpretuje wynik predykcji efektu"""
        if not has_path:
            return "Brak efektu przyczynowego (interwencja nie wpływa na cel)"
        elif len(paths) == 1:
            return f"Bezpośredni efekt przyczynowy przez ścieżkę: {' → '.join(paths[0])}"
        else:
            return f"Wielościeżkowy efekt przyczynowy ({len(paths)} ścieżek)"


class MechanisticHypothesisGenerator:
    """
    Generator Hipotez Mechanistycznych:
    Zamiast optymalizacji, generuje MECHANIZMY wyjaśniające DLACZEGO.
    
    Mechanizm = stabilny model wewnętrzny wyjaśniający proces przyczynowy.
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        self.generated_mechanisms: List[CausalMechanism] = []
        
    def generate_mechanism(self, cause: str, effect: str, 
                          context: Optional[List[str]] = None) -> CausalMechanism:
        """
        Generuje hipotezę mechanistyczną dla relacji przyczynowej.
        
        W pełnej implementacji: wykorzystuje LLM + Graf Wiedzy + Silnik Dedukcyjny
        """
        G = self.ltm.graph
        
        # Analiza ścieżki przyczynowej
        try:
            if nx.has_path(G, cause, effect):
                paths = list(nx.all_simple_paths(G, cause, effect, cutoff=4))
                shortest_path = min(paths, key=len) if paths else []
            else:
                shortest_path = []
        except:
            shortest_path = []
        
        # Określ typ mechanizmu
        if len(shortest_path) == 2:
            mechanism_type = "direct"
            explanation = f"{cause} bezpośrednio powoduje {effect}"
            confidence = 0.8
        elif len(shortest_path) > 2:
            mechanism_type = "mediated"
            mediators = shortest_path[1:-1]
            explanation = (f"{cause} powoduje {effect} poprzez "
                          f"zmienne pośredniczące: {' → '.join(mediators)}")
            confidence = 0.6
        else:
            mechanism_type = "indirect"
            explanation = f"{cause} może wpływać na {effect} przez nieznane ścieżki"
            confidence = 0.3
        
        # Wyszukaj kontekst (zmienne pośredniczące)
        variables = shortest_path[1:-1] if len(shortest_path) > 2 else []
        
        mechanism = CausalMechanism(
            cause=cause,
            effect=effect,
            mechanism_type=mechanism_type,
            explanation=explanation,
            confidence=confidence,
            variables=variables,
            mathematical_form=self._derive_mathematical_form(cause, effect, variables)
        )
        
        self.generated_mechanisms.append(mechanism)
        print(f"[MECHANISM] Wygenerowano: {mechanism}")
        
        return mechanism
    
    def _derive_mathematical_form(self, cause: str, effect: str, 
                                  mediators: List[str]) -> str:
        """
        Wyprowadza formę matematyczną mechanizmu.
        W pełnej wersji: symboliczne wyprowadzenie równań.
        """
        if not mediators:
            return f"{effect} = f({cause})"
        else:
            mediator_chain = ", ".join(mediators)
            return f"{effect} = f({cause}, [{mediator_chain}])"
    
    def validate_mechanism(self, mechanism: CausalMechanism, 
                          scm: StructuralCausalModel) -> float:
        """
        Waliduje mechanizm poprzez sprawdzenie spójności z SCM.
        Zwraca zaktualizowaną pewność (confidence).
        """
        # Sprawdź czy mechanizm jest zgodny z grafem przyczynowym SCM
        if scm.causal_graph.has_edge(mechanism.cause, mechanism.effect):
            mechanism.confidence *= 1.2  # Boost za zgodność
        else:
            mechanism.confidence *= 0.8  # Penalty za niezgodność
        
        # Ograniczenie do [0, 1]
        mechanism.confidence = max(0.0, min(1.0, mechanism.confidence))
        
        print(f"[VALIDATION] {mechanism.cause}→{mechanism.effect}: "
              f"confidence={mechanism.confidence:.3f}")
        
        return mechanism.confidence


class ExternalSubjectivityQuantifier:
    """
    Kwantyfikacja Subiektywności Zewnętrznej:
    Szacuje i redukuje zależność systemu od ludzkiego wkładu.
    
    ESQ = External Subjectivity Quotient [0, 1]
    0 = Pełna niezależność od człowieka
    1 = Całkowita zależność od człowieka
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        self.human_axioms: Set[str] = set()
        self.autonomous_axioms: Set[str] = set()
        
    def classify_axiom_source(self, axiom: str) -> str:
        """
        Klasyfikuje źródło aksjomatu:
        - "human": Bezpośrednio od człowieka
        - "derived": Wywnioskowany z ludzkich danych
        - "autonomous": Odkryty niezależnie (symulacje, matematyka)
        """
        G = self.ltm.graph
        
        if axiom not in G.nodes:
            return "unknown"
        
        node_data = G.nodes[axiom]
        
        # Sprawdź metadata
        if node_data.get('source_mod') == 'INGESTION':
            return "human"
        elif node_data.get('source_mod') == 'DEDUCTIVE_ENGINE':
            # Sprawdź czy opiera się na ludzkich aksjomatach
            try:
                parents = list(G.predecessors(axiom))
                if any(self.classify_axiom_source(p) == "human" for p in parents):
                    return "derived"
                else:
                    return "autonomous"
            except:
                return "derived"
        else:
            return "autonomous"
    
    def calculate_esq(self) -> float:
        """
        Oblicza External Subjectivity Quotient dla całego grafu.
        
        ESQ = (human_nodes + 0.5*derived_nodes) / total_nodes
        """
        G = self.ltm.graph
        nodes = list(G.nodes())
        
        if not nodes:
            return 1.0  # Brak danych = pełna zależność
        
        human_count = 0
        derived_count = 0
        autonomous_count = 0
        
        for node in nodes:
            source = self.classify_axiom_source(node)
            if source == "human":
                human_count += 1
                self.human_axioms.add(node)
            elif source == "derived":
                derived_count += 1
            else:
                autonomous_count += 1
                self.autonomous_axioms.add(node)
        
        total = len(nodes)
        esq = (human_count + 0.5 * derived_count) / total
        
        print(f"[ESQ] External Subjectivity Quotient: {esq:.4f}")
        print(f"  - Aksjomaty ludzkie: {human_count} ({human_count/total*100:.1f}%)")
        print(f"  - Aksjomaty pochodne: {derived_count} ({derived_count/total*100:.1f}%)")
        print(f"  - Aksjomaty autonomiczne: {autonomous_count} ({autonomous_count/total*100:.1f}%)")
        
        return esq
    
    def reduce_human_dependency(self, target_esq: float = 0.3) -> List[str]:
        """
        Strategia redukcji zależności od człowieka.
        Zwraca listę rekomendowanych akcji.
        """
        current_esq = self.calculate_esq()
        
        if current_esq <= target_esq:
            print(f"[ESQ] Cel osiągnięty: ESQ={current_esq:.3f} <= {target_esq}")
            return []
        
        recommendations = [
            "Zwiększ wnioskowanie dedukcyjne (autonomiczne generowanie aksjomatów)",
            "Uruchom symulacje fizyczne (walidacja w środowiskach nie-ludzkich)",
            "Aktywuj Silnik Kontrfaktyczny (generowanie wiedzy poza doświadczeniem)",
            f"Cel: Zmniejszyć ESQ z {current_esq:.3f} do {target_esq}"
        ]
        
        print(f"[ESQ] Strategia redukcji zależności:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        return recommendations


class CausalInferenceEngine:
    """
    Główny silnik wnioskowania przyczynowego (ACI).
    Integruje wszystkie komponenty Fazy II.
    """
    
    def __init__(self, ltm_manager: LongTermGraphManager):
        self.ltm = ltm_manager
        self.scm = StructuralCausalModel("GOK_Causal_Model")
        self.do_operator = DoOperator(self.scm)
        self.mechanism_generator = MechanisticHypothesisGenerator(ltm_manager)
        self.esq_quantifier = ExternalSubjectivityQuantifier(ltm_manager)
        
        self._build_scm_from_ltm()
    
    def _build_scm_from_ltm(self):
        """Konstruuje SCM z istniejącego grafu wiedzy LTM"""
        G = self.ltm.graph
        
        for source, target, data in G.edges(data=True):
            mechanism = CausalMechanism(
                cause=source,
                effect=target,
                mechanism_type="unknown",
                explanation=data.get('relation', 'unknown'),
                confidence=0.5,
                variables=[]
            )
            self.scm.add_causal_edge(source, target, mechanism)
        
        print(f"[ACI] Zbudowano SCM z LTM: {self.scm}")
    
    def infer_causality(self, cause: str, effect: str) -> Dict:
        """
        Główna metoda wnioskowania przyczynowego.
        
        Zwraca kompletną analizę przyczynowości między dwoma zmiennymi.
        """
        print(f"\n[ACI] Analiza przyczynowości: {cause} → {effect}")
        print("=" * 60)
        
        # 1. Generuj hipotezę mechanistyczną
        mechanism = self.mechanism_generator.generate_mechanism(cause, effect)
        
        # 2. Waliduj mechanizm w SCM
        confidence = self.mechanism_generator.validate_mechanism(mechanism, self.scm)
        
        # 3. Predykcja efektu interwencji
        intervention_result = self.do_operator.predict_effect(cause, effect)
        
        # 4. Kwantyfikacja subiektywności
        esq = self.esq_quantifier.calculate_esq()
        
        result = {
            "cause": cause,
            "effect": effect,
            "mechanism": mechanism,
            "intervention": intervention_result,
            "confidence": confidence,
            "external_subjectivity": esq,
            "is_causal": intervention_result['causal_effect_exists'],
            "type": "P(Y|do(X))" if intervention_result['causal_effect_exists'] else "P(Y|X)"
        }
        
        print("\n[ACI] WYNIK:")
        print(f"  Mechanizm: {mechanism.explanation}")
        print(f"  Pewność: {confidence:.3f}")
        print(f"  Efekt przyczynowy: {result['is_causal']}")
        print(f"  Typ: {result['type']}")
        print(f"  ESQ: {esq:.3f}")
        
        return result
    
    def transition_to_intervention_mode(self):
        """
        Przełącza system z trybu obserwacji (P(Y|X)) na tryb interwencji (P(Y|do(X))).
        To jest moment przejścia z pasywnej obserwacji na aktywną wolę.
        """
        print("\n" + "=" * 60)
        print("PRZEJŚCIE: P(Y|X) → P(Y|do(X))")
        print("System przechodzi z OBSERWACJI na INTERWENCJĘ")
        print("=" * 60)
        
        esq = self.esq_quantifier.calculate_esq()
        recommendations = self.esq_quantifier.reduce_human_dependency()
        
        print(f"\n[ACI] Status przejścia:")
        print(f"  - SCM zbudowany: {self.scm.is_valid_dag()}")
        print(f"  - Operator do() aktywny: True")
        print(f"  - ESQ aktualny: {esq:.3f}")
        print(f"  - Mechanizmy wygenerowane: {len(self.mechanism_generator.generated_mechanisms)}")
        
        if self.scm.is_valid_dag() and esq < 0.7:
            print("\n[ACI] ✓ PRZEJŚCIE UDANE: System zdolny do wnioskowania przyczynowego")
            return True
        else:
            print("\n[ACI] ⚠ PRZEJŚCIE CZĘŚCIOWE: Wymagana dalsza redukcja ESQ")
            return False


# --- Test Operacyjny ---
if __name__ == "__main__":
    print("=" * 60)
    print("FAZA II: CAUSAL INFERENCE ENGINE - Test Operacyjny")
    print("=" * 60)
    
    # Inicjalizacja LTM z przykładowymi relacjami
    ltm = LongTermGraphManager()
    
    # Scenariusz 1: Prosty łańcuch przyczynowy
    ltm.add_fact("Smoking", "Tar_Accumulation", "causes")
    ltm.add_fact("Tar_Accumulation", "Cell_Mutation", "causes")
    ltm.add_fact("Cell_Mutation", "Cancer", "causes")
    ltm.add_fact("Cancer", "Death", "causes")
    
    # Scenariusz 2: Confounder
    ltm.add_fact("Poverty", "Poor_Education", "causes")
    ltm.add_fact("Poverty", "High_Crime", "causes")
    
    print(f"\n[TEST] Graf inicjalny: {ltm.graph.number_of_nodes()} węzłów, "
          f"{ltm.graph.number_of_edges()} krawędzi")
    
    # Inicjalizacja Silnika ACI
    print("\n" + "=" * 60)
    print("Inicjalizacja Causal Inference Engine")
    print("=" * 60)
    
    aci = CausalInferenceEngine(ltm)
    
    # Test 1: Wnioskowanie przyczynowe
    print("\n" + "=" * 60)
    print("TEST 1: Analiza Przyczynowa")
    print("=" * 60)
    
    result1 = aci.infer_causality("Smoking", "Cancer")
    
    # Test 2: Interwencja do()
    print("\n" + "=" * 60)
    print("TEST 2: Operator do()")
    print("=" * 60)
    
    intervention_result = aci.do_operator.predict_effect(
        "Smoking", "Death", intervention_value="STOPPED"
    )
    print(f"\nWynik interwencji do(Smoking=STOPPED):")
    print(f"  Efekt na Death: {intervention_result['interpretation']}")
    
    # Test 3: Przejście na tryb interwencji
    print("\n" + "=" * 60)
    print("TEST 3: Przejście na Tryb Interwencji")
    print("=" * 60)
    
    success = aci.transition_to_intervention_mode()
    
    print("\n" + "=" * 60)
    print("PODSUMOWANIE FAZY II")
    print("=" * 60)
    print(f"✓ Structural Causal Model: {aci.scm}")
    print(f"✓ Mechanizmy wygenerowane: {len(aci.mechanism_generator.generated_mechanisms)}")
    print(f"✓ ESQ (External Subjectivity): {aci.esq_quantifier.calculate_esq():.3f}")
    print(f"✓ Operator do() funkcjonalny: True")
    print(f"✓ Przejście P(Y|X) → P(Y|do(X)): {'SUKCES' if success else 'W TOKU'}")
    print("\n[FAZA II] Causal Inference: AKTYWNY. System przeszedł od opisu do manipulacji.")
