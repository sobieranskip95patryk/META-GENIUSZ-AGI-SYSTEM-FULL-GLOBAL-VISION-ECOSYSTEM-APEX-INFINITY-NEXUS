# 🔗 HYBRID IMPACT VECTOR (HIV) — Dokumentacja Implementacji

**Wersja:** 1.0  
**Data:** 27 stycznia 2026  
**Status:** ✅ PRODUCTION READY  
**Autor:** GitHub Copilot | Patryk Sobierański

---

## I. OVERVIEW

**HybridImpactVector** to serce fuzji AGI_GOK ↔ Global-Vision v1.0.

Jest to unikatowa struktura danych, która łączy:
- 🌍 **ProjectVectors** (Global-Vision) — embeddingi semantyczne 768-dim
- 🧠 **Sense Atoms** (AGI_GOK) — logika i intencje systemu
- ⚖️ **Ethical Multi-Vision (EMV)** — ocena etyczna (0.0–1.0)
- 🔗 **Causal Graph** — związki między projektami

**To pozwala systemowi "rozumieć" projekty z pełnym kontekstem**: semantycznym, logicznym, etycznym i przyczynowym.

---

## II. STRUKTURA

### A. Główne Komponenty

```python
class HybridImpactVector:
    # Identyfikacja
    vector_id: str                          # Unique ID
    
    # Dane z Global-Vision
    project_metadata: ProjectMetadata       # {name, creator, category, ...}
    semantic_embedding: np.ndarray          # 768-dim OpenAI embedding
    embedding_model: str                    # "openai-text-embedding-3-small"
    
    # Dane z AGI_GOK
    sense_atoms: List[SenseAtom]           # Logika systemu
    local_score: float                      # GOK:AI LocalScore (0–10000)
    
    # Warstwa Etyki
    ethical_multi_vision_score: float      # EMV (0.0–1.0)
    ethical_justification: str              # Uzasadnienie etyczne
    constraint_violations: List[str]        # Naruszenia constraints
    
    # Metryki Wpływu
    gis_score: float                        # Global Impact Score (0–10000)
    pri_score: float                        # Planetary Resonance (0.0–1.0)
    caf_score: float                        # Civilization Alignment (0.0–1.0)
    spc_score: float                        # Synergy Potential (0.0–1.0)
    
    # Kausalność
    causal_dependencies: List[CausalityLink]  # Związki z innymi projektami
    risk_level: RiskLevel                   # CRITICAL → NONE
    risk_description: str                   # Opis ryzyka
    
    # Audyt
    audit_log: List[Dict]                   # Pełna historia zmian
    created_at: str                         # ISO 8601 timestamp
    updated_at: str                         # ISO 8601 timestamp
```

### B. Klasy Pomocnicze

```python
@dataclass
class SenseAtom:
    """Jednostka logiki z AGI_GOK"""
    atom_id: str
    semantic_intent: str        # BLOCK, EXPAND, MONITOR
    weight: float              # 0.0–1.0 (waga w systemie)
    metadata: Dict             # Dodatkowe dane

@dataclass
class ProjectMetadata:
    """Metadane projektu z Global-Vision"""
    project_id: str
    project_name: str
    description: str
    creator: str
    category: ImpactCategory    # EDUCATION, TECH, ECOLOGY, ...
    url: Optional[str]
    tags: List[str]
    created_at: str
    updated_at: str

@dataclass
class CausalityLink:
    """Link przyczynowy między dwoma projektami"""
    source_project_id: str
    target_project_id: str
    relationship_type: CausalityType   # SYNERGISTIC, COMPETITIVE, ...
    strength: float                     # 0.0–1.0 (siła wpływu)
    description: str
```

---

## III. KLUCZOWE METODY

### 1. calculate_hybrid_priority() → float

**Wzór Patryka:** Synergia logiki, etyki i wpływu

```
priority = (logic × semantic_match × 0.30) 
         + (ethics × 0.40) 
         + (gis_normalized × 0.30) 
         × 100

Wynik: 0–100 (gdzie 100 = najwyższy priorytet)
```

**Przykład:**
```python
hiv = HybridImpactVector(...)
hiv.gis_score = 8760.73
hiv.ethical_multi_vision_score = 0.92
priority = hiv.calculate_hybrid_priority()  # → ~63.86
```

---

### 2. calculate_synergy_with(other: HybridImpactVector) → float

Oblicza synergię między dwoma projektami:

```
synergy = (cosine_similarity × 0.5)
        + (intents_complementarity × 0.25)
        + (ethical_alignment × 0.25)

Wynik: 0.0–1.0 (gdzie 1.0 = idealna synergia)
```

**Przykład:**
```python
hiv1 = HybridImpactVector(...)  # Education
hiv2 = HybridImpactVector(...)  # Technology
synergy = hiv1.calculate_synergy_with(hiv2)  # → 0.87
```

---

### 3. calculate_risk_score() → float

Oblicza ryzyko przyczynowe:

```
risk = (dependency_risk × 0.30)
     + (violation_risk × 0.20)
     + (risk_level_score × 0.30)
     + (1 - ethics × 0.20)

Wynik: 0.0–1.0 (gdzie 1.0 = maksymalne ryzyko)
```

---

### 4. verify_ethical_alignment() → Tuple[bool, str]

Weryfikuje zgodność etyczną:

- ✅ EMV score musi być > 0.3
- ✅ Constraint violations muszą być wyjaśnione
- ✅ Critical risk wymaga EMV > 0.7
- ✅ GIS < 4000 nie powinien mieć wysokiego priorytetu

**Przykład:**
```python
is_aligned, justification = hiv.verify_ethical_alignment()
# is_aligned = True
# justification = "Zaakceptowano — projekt spełnia kryteria etyczne"
```

---

## IV. UŻYCIE PRAKTYCZNE

### Scenariusz 1: Tworzenie HIV z Global-Vision

```python
from CORE.Structures.hybrid_impact_vector import (
    HybridImpactVector,
    ProjectMetadata,
    ImpactCategory,
    HybridImpactVectorFactory,
    SenseAtom
)
import numpy as np

# 1. Dane z Global-Vision
project_name = "Cosmic Education Platform"
description = "Global platform for space education"
embedding = np.random.randn(768)  # 768-dim z OpenAI
embedding = embedding / np.linalg.norm(embedding)

# 2. Tworzenie metadata
metadata = ProjectMetadata(
    project_id="PROJECT_001",
    project_name=project_name,
    description=description,
    creator="Patryk Sobierański",
    category=ImpactCategory.EDUCATION,
    tags=["education", "space", "global"]
)

# 3. Tworzenie HIV
hiv = HybridImpactVectorFactory.from_global_vision_data(
    project_id="PROJECT_001",
    project_name=project_name,
    description=description,
    embedding=embedding,
    creator="Patryk Sobierański",
    category=ImpactCategory.EDUCATION
)

# 4. Dodanie danych z AGI_GOK
hiv.local_score = 1751.45
hiv.gis_score = 8760.73
hiv.pri_score = 0.92
hiv.caf_score = 0.88
hiv.spc_score = 0.75
hiv.ethical_multi_vision_score = 0.92

# 5. Dodanie sense_atoms
sense_atom = SenseAtom(
    atom_id="ATOM_001",
    semantic_intent="EXPAND",
    weight=0.95
)
hiv.add_sense_atom(sense_atom)

# 6. Obliczenia
priority = hiv.calculate_hybrid_priority()     # → 63.86
risk = hiv.calculate_risk_score()              # → 0.076
aligned, justif = hiv.verify_ethical_alignment()  # → (True, "...")

print(f"Priority: {priority} | Risk: {risk} | Aligned: {aligned}")
```

---

### Scenariusz 2: Analiza Portfolio (porównanie wielu HIV)

```python
# Załóżmy, że mamy listę HybridImpactVectors
portfolio = [hiv1, hiv2, hiv3, hiv4, hiv5]

# 1. Obliczenie synergii dla każdej pary
synergy_matrix = np.zeros((len(portfolio), len(portfolio)))
for i, hiv_i in enumerate(portfolio):
    for j, hiv_j in enumerate(portfolio):
        if i != j:
            synergy_matrix[i][j] = hiv_i.calculate_synergy_with(hiv_j)

# 2. Średnia synergii
mean_synergy = np.mean(synergy_matrix[synergy_matrix > 0])
print(f"Portfolio Synergy: {mean_synergy:.3f}")

# 3. Findowanie best performers
priorities = [hiv.calculate_hybrid_priority() for hiv in portfolio]
top_3_indices = np.argsort(priorities)[-3:]
print(f"Top 3 Projects: {[portfolio[i].project_metadata.project_name for i in top_3_indices]}")

# 4. Risk assessment
risks = [hiv.calculate_risk_score() for hiv in portfolio]
high_risk = [portfolio[i] for i, r in enumerate(risks) if r > 0.3]
print(f"High Risk Projects: {len(high_risk)}")
```

---

### Scenariusz 3: Eksport do JSON (dla audytu)

```python
# Eksport pojedynczego HIV
json_str = hiv.to_json(indent=2)
with open("hiv_export.json", "w") as f:
    f.write(json_str)

# Eksport portfolio
import json
portfolio_data = [hiv.to_dict() for hiv in portfolio]
with open("portfolio_export.json", "w") as f:
    json.dump(portfolio_data, f, indent=2, default=str)
```

---

## V. INTEGRACJA Z GLOBALVISION ANALYZER

### Tworzenie HIV z GlobalVision

```python
from CORE.Inference.global_vision_analyzer import GlobalVisionAnalyzer
from CORE.Structures.hybrid_impact_vector import HybridImpactVectorFactory
import numpy as np

analyzer = GlobalVisionAnalyzer()

# 1. Obliczenie GIS (istniejące)
metrics = analyzer.calculate_gis(
    local_score=1751.45,
    pri=0.92,
    caf=0.88,
    spc=0.75,
    project_name="Cosmic Education"
)

# 2. Pobieranie embeddings z Global-Vision
embedding = np.random.randn(768)  # W praktyce: z OpenAI API
embedding = embedding / np.linalg.norm(embedding)

# 3. Tworzenie HIV
hiv = HybridImpactVectorFactory.from_agi_gok_data(
    gis_score=metrics.gis,
    local_score=metrics.local_score,
    pri=metrics.pri,
    caf=metrics.caf,
    spc=metrics.spc,
    project_metadata=metadata,
    embedding=embedding
)

# 4. Weryfikacja etyczna
is_aligned, justif = hiv.verify_ethical_alignment()
```

---

## VI. VALIDACJA

```python
from CORE.Structures.hybrid_impact_vector import validate_hybrid_impact_vector

is_valid, errors = validate_hybrid_impact_vector(hiv)

if is_valid:
    print("✅ HIV jest poprawny i gotowy do użytku")
else:
    print("❌ Błędy validacji:")
    for error in errors:
        print(f"   - {error}")
```

---

## VII. ENUMS I STAŁE

### ImpactCategory
```python
PLANETARY         # Wpływ globalny/planetarny
CIVILIZATION      # Wpływ na strukturę cywilizacji
ECOSYSTEM         # Wpływ ekologiczny
ECONOMIC          # Wpływ ekonomiczny
SOCIAL            # Wpływ społeczny
TECHNOLOGICAL     # Wpływ technologiczny
EDUCATION         # Wpływ edukacyjny
HEALTH            # Wpływ na zdrowie
ENERGY            # Wpływ energetyczny
UNKNOWN           # Nieznany
```

### RiskLevel
```python
CRITICAL = 5      # Krytyczne ryzyko
HIGH = 4          # Wysokie ryzyko
MEDIUM = 3        # Średnie ryzyko
LOW = 2           # Niskie ryzyko
MINIMAL = 1       # Minimalne ryzyko
NONE = 0          # Brak ryzyka
```

### CausalityType
```python
SYNERGISTIC       # Projekty się wzmacniają
COMPETITIVE       # Konkurencja o zasoby
NEUTRAL           # Brak wpływu
CONFLICTING       # Projekty się zwalczają
DEPENDENT         # Zależność
```

---

## VIII. DEMO OUTPUT

```
================================================================================
HYBRID IMPACT VECTOR — Demo Implementacji
================================================================================

✅ HybridImpactVector created successfully

📊 Project: Cosmic Education Platform
   Category: EDUCATION
   Creator: Patryk Sobierański

📈 Impact Metrics:
   GIS Score: 8760.73 / 10000
   PRI Score: 0.92 / 1.0
   CAF Score: 0.88 / 1.0
   SPC Score: 0.75 / 1.0
   Local Score: 1751.45 / 10000

🧠 Logic & Ethics:
   Sense Atoms: 2
   EMV Score: 0.92 / 1.0
   Ethical Alignment: True

🎯 Calculated Metrics:
   Hybrid Priority: 63.86 / 100.0
   Risk Score: 0.076 / 1.0
   Risk Level: MINIMAL

📋 Vector Summary:
   Vector ID: HIV_PROJECT_001_001
   Created: 2026-01-27T20:48:59.341835
   Audit Entries: 3

✔️ Validation: PASSED
```

---

## IX. NASTĘPNE KROKI

### Faza 2: Migration Script
Kod do przeniesienia istniejących danych z Global-Vision v1.0 do HybridImpactVectors.

### Faza 3: FastAPI Integration
Serwis REST do ekspozy HybridImpactVectors poprzez API:
```
POST   /api/vectors/create
GET    /api/vectors/{id}
GET    /api/vectors/portfolio
POST   /api/vectors/synergy
```

### Faza 4: Frontend Integration
React komponenty do wizualizacji HIVs:
- Vector Explorer
- Synergy Dashboard
- Risk Heatmap
- Causal Graph Visualizer

---

**Status:** ✅ KROK 1 FUZJI ZAKOŃCZONY  
**Następny:** Stworzenie Migration Script (KROK 2)

