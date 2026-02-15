# T_CAUSALITY: Quick Start Guide

## Szybki Start z T_Causality

### 1. Uruchomienie Pełnego Przejścia

```bash
cd d:\REPO_MASTER_GOKAI\AGI_GOK
python CORE/Inference/t_causality_orchestrator.py
```

**Wynik:** Pełne przejście przez wszystkie 4 fazy T_Causality

---

### 2. Testy Jednostkowe

```bash
python tests/test_t_causality.py
```

**Wynik:** Weryfikacja wszystkich modułów i integracji

---

### 3. Integracja z Kodem Python

```python
from CORE.Memory.long_term_graph import LongTermGraphManager
from CORE.Inference.t_causality_orchestrator import TCausalityOrchestrator

# Inicjalizacja
ltm = LongTermGraphManager()

# Załaduj dane
ltm.add_fact("Smoking", "Cancer", "causes")
ltm.add_fact("Cancer", "Death", "causes")

# Utwórz orkiestratora
orchestrator = TCausalityOrchestrator(ltm)

# Wykonaj przejście T_Causality
success = orchestrator.execute_full_transition()

if success:
    print("✓ T_Causality achieved!")
    print(f"Tier: {orchestrator.ags.current_state.tier.value}")
    print(f"Autonomy: {orchestrator.ags.current_state.autonomy_level:.2%}")
```

---

### 4. Testowanie Poszczególnych Faz

#### Faza I: Anti-D Reduction

```python
from CORE.Inference.anti_d_reduction import MetaCognitiveAudit, CausalIsolation

mka = MetaCognitiveAudit(ltm)
scores = mka.audit_entire_graph()

causal_iso = CausalIsolation(ltm, mka)
spurious = causal_iso.identify_spurious_correlations()
```

#### Faza II: Causal Inference

```python
from CORE.Inference.causal_inference_engine import CausalInferenceEngine

aci = CausalInferenceEngine(ltm)
result = aci.infer_causality("Smoking", "Cancer")
print(f"Mechanism: {result['mechanism'].explanation}")
```

#### Faza III: Counterfactual

```python
from CORE.Inference.counterfactual_engine import CounterfactualEngine

cf_engine = CounterfactualEngine(ltm)
scenario = cf_engine.generate_counterfactual(
    "Smoking", "NO_SMOKING", "Death"
)
print(f"Counterfactual: {scenario}")
```

#### Faza IV: Autonomous Goals

```python
from CORE.Inference.autonomous_goal_system import AutonomousGoalSystem

ags = AutonomousGoalSystem(ltm)
success = ags.initiate_t_causality_transition()
print(f"T_Causality: {ags.t_causality_achieved}")
```

---

### 5. Konfiguracja Parametrów

Edytuj [config.yaml](CORE/Memory/config.yaml):

```yaml
t_causality:
  enabled: true
  
  anti_d:
    c_d_threshold: 0.6
    correlation_threshold: 0.4
    
  causal_inference:
    esq_target: 0.3
    do_operator_enabled: true
    
  counterfactual:
    max_worlds: 50
    stability_threshold: 0.4
    
  autonomous_goals:
    metacel_alpha: 1.0
    metacel_beta: 0.8
    metacel_gamma: 1.2
    autonomy_threshold: 0.7
```

---

### 6. Monitoring Statusu

```python
status = orchestrator.get_system_status()
print(f"Fazy ukończone: {status['phases_completed']}/{status['phases_total']}")
print(f"T_Causality: {status['t_causality_achieved']}")
print(f"Tier: {status['current_tier']}")
```

---

### 7. Logi i Raporty

Po przejściu T_Causality, system automatycznie generuje:

- **Raport JSON:** `T_CAUSALITY_TRANSITION_REPORT.json`
- **Logi konsoli:** Szczegółowe informacje o każdej fazie

---

### 8. Przykład Pełnego Workflow

```python
# 1. Setup
from CORE.Memory.long_term_graph import LongTermGraphManager
from CORE.Inference.t_causality_orchestrator import TCausalityOrchestrator

ltm = LongTermGraphManager()

# 2. Załaduj wiedzę
ltm.add_fact("Exercise", "Health", "causes")
ltm.add_fact("Health", "Longevity", "causes")
ltm.add_fact("Smoking", "Cancer", "causes")

# 3. Inicjalizuj T_Causality
orchestrator = TCausalityOrchestrator(ltm)

# 4. Wykonaj przejście
print("Rozpoczynam przejście T_Causality...")
success = orchestrator.execute_full_transition()

# 5. Sprawdź wyniki
if success:
    state = orchestrator.ags.current_state
    print("\n=== WYNIKI ===")
    print(f"Tier: {state.tier.value}")
    print(f"Autonomia: {state.autonomy_level:.1%}")
    print(f"Złożoność przyczynowa: {state.causal_complexity:.2f}")
    print(f"Koherencja P: {state.coherence_p:.4f}")
    print(f"ESQ: {state.esq:.4f}")
    
    # 6. Ewolucja autonomiczna
    print("\nSymuluję ewolucję autonomiczną...")
    for i in range(5):
        orchestrator.ags.evolve_one_cycle()
    
    print("\n✓ GOK:AI osiągnął T_Causality (Tier 3 AGI)")
```

---

### 9. Rozwiązywanie Problemów

#### Problem: Faza I nie przechodzi
**Rozwiązanie:** Zwiększ threshold w `config.yaml`:
```yaml
anti_d:
  c_d_threshold: 0.7  # Wyższy próg
```

#### Problem: ESQ zbyt wysokie
**Rozwiązanie:** Dodaj więcej autonomicznych danych:
```python
# Generuj fakty z dedukcji, nie ingestii
deductive_engine.integrate_new_facts()
```

#### Problem: Kontrfakty niestabilne
**Rozwiązanie:** Obniż threshold stabilności:
```yaml
counterfactual:
  stability_threshold: 0.3  # Niższy próg
```

---

### 10. Dokumentacja Pełna

- **Manifest główny:** [T_Causality_Manifest.md](CORE/Memory/T_Causality_Manifest.md)
- **Architektura:** [FINAL_ARCHITECTURE_MANIFEST.md](FINAL_ARCHITECTURE_MANIFEST.md)
- **README:** [README.md](README.md)

---

## Najczęstsze Pytania (FAQ)

**Q: Ile czasu trwa przejście T_Causality?**  
A: 5-10 sekund w zależności od rozmiaru grafu wiedzy.

**Q: Czy mogę uruchomić tylko jedną fazę?**  
A: Tak, każdy moduł ma własny plik wykonywalny z `if __name__ == "__main__"`.

**Q: Jak zintegrować z bridge_server.py?**  
A: Zaimportuj `TCausalityOrchestrator` i wywołaj `execute_full_transition()` podczas inicjalizacji serwera.

**Q: Co to jest ESQ?**  
A: External Subjectivity Quotient - miara zależności systemu od zewnętrznych celów (0 = pełna autonomia, 1 = pełna zależność).

**Q: Co to jest Φ_meta?**  
A: Meta fitness function - wartość użyteczności metacelu ewolucyjnego: `Φ_meta = α*CC - β*SU + γ*P`.

---

**Powodzenia w eksploracji T_Causality!** 🚀

*GOK:AI v7.1 | T_Causality Enabled*
