# GlobalVision: Przewodnik Techniczny dla Developerów

**Wersja:** 1.0  
**Data:** 27 stycznia 2026  
**Autor:** META-GENIUSZ® (Patryk Sobierański)

---

## 1. Przegląd

GlobalVision to **czysto analityczny system** do oceny wpływu projektów na skalę planetarną. Nie jest to system autonomiczny — wszystkie wyniki to rekomendacje dla decydentów.

### Cechy:
- ✅ **Przejrzyste algorytmy** — wszystkie obliczenia są audytowalne
- ✅ **Brak autonomii** — system nie podejmuje decyzji ani działań
- ✅ **Modułowy** — można łatwo rozszerzać i testować
- ✅ **Offline-first** — działa w całości lokalnie

---

## 2. Instalacja

### Wymagania
- Python 3.10+
- Brak zewnętrznych zależności (pure Python)

### Setup
```bash
cd e:\REPO_MASTER_GOKAI\AGI_GOK

# (opcjonalnie) Utwórz venv
python -m venv .venv
.venv\Scripts\activate

# Moduł jest już dostępny w CORE/Inference/
python CORE/Inference/global_vision_analyzer.py
```

---

## 3. Architektura modułu

```
global_vision_analyzer.py
├── PlanetaryImpactMetrics (dataclass)
│   └── Przechowuje wyniki: GIS, PRI, CAF, SPC
│
├── GlobalVisionAnalyzer (klasa główna)
│   ├── calculate_gis()          # Obliczenie wyniku GIS
│   ├── get_recommendation()     # Rekomendacja strategiczna
│   ├── batch_analyze()          # Analiza portfolio
│   ├── export_audit_log()       # Eksport dla audytu
│   └── _internal helpers        # Funkcje wewnętrzne
│
└── DEMO + TESTY (main block)
```

---

## 4. Kluczowe komponenty

### 4.1 PlanetaryImpactMetrics

**Rola:** Przechowuje wyniki obliczeń.

```python
metrics = PlanetaryImpactMetrics(
    local_score=1751.45,      # GOK:AI wynik (0–2000)
    pri=0.92,                 # Planetary Resonance Index
    caf=0.88,                 # Civilization Alignment Factor
    spc=0.75,                 # Synergy Potential Coefficient
    gis=8760.73,              # Wynik finalny (0–10000)
    project_name="Project X", # Metadane
    creator_name="Alice",
    domain="Education",
    timestamp="2026-01-27T...",
)
```

### 4.2 GlobalVisionAnalyzer

**Główna klasa** zawierająca logikę analiz.

#### Wagi strategiczne (przejrzyste, audytowalne):
```python
WEIGHT_PRI = 0.40   # Wartości i rezonans
WEIGHT_CAF = 0.35   # Kierunek cywilizacyjny
WEIGHT_SPC = 0.15   # SynergIA
WEIGHT_LS = 0.10    # Potencjał lokalny
# Suma = 1.0 (zawsze spójne)
```

#### Progi decyzyjne (przejrzyste):
```python
THRESHOLD_GLOBAL_SCALE = 8500   # Skalowanie globalne
THRESHOLD_HIGH_POTENTIAL = 6500 # Wysoki potencjał
THRESHOLD_LOCAL_RELEVANCE = 4000 # Znaczenie lokalne
```

---

## 5. Interfejs API

### 5.1 `calculate_gis()` — Obliczanie wpływu

```python
analyzer = GlobalVisionAnalyzer()

metrics = analyzer.calculate_gis(
    local_score=1751.45,
    pri=0.92,
    caf=0.88,
    spc=0.75,
    project_name="Cosmic Education",
    creator_name="Alice Smith",
    domain="Education",
)

# Rezultat: PlanetaryImpactMetrics
print(metrics.gis)  # 8760.73
print(metrics.to_dict())  # Słownik dla serializacji
```

**Parametry:**
- `local_score`: float [0–2000] – wynik z GOK:AI
- `pri`: float [0.0–1.0] – Planetary Resonance Index
- `caf`: float [0.0–1.0] – Civilization Alignment Factor
- `spc`: float [0.0–1.0] – Synergy Potential Coefficient
- `project_name`, `creator_name`, `domain`: str – metadane

**Zwraca:** `PlanetaryImpactMetrics` z obliczonym GIS

**Wzór:**
```
GIS = ((PRI × 0.40) + (CAF × 0.35) + (SPC × 0.15) + (norm_LS × 0.10)) × 10000
```

---

### 5.2 `get_recommendation()` — Rekomendacja strategiczna

```python
rec = analyzer.get_recommendation(metrics)

# Słownik z:
# - recommendation_level: "GLOBAL_SCALE" | "HIGH_POTENTIAL" | "LOCAL_RELEVANCE" | "REVIEW_NEEDED"
# - explanation: str – uzasadnienie
# - action_items: List[str] – sugerowane kroki
# - risk_factors: List[str] – zidentyfikowane ryzyka
# - synergy_opportunities: List[str] – możliwości wspólpracy
# - disclaimer: str – „Wszystkie decyzje pod kontrolą człowieka"
```

**Przykład wyjścia:**
```json
{
  "recommendation_level": "GLOBAL_SCALE",
  "gis": 8760.73,
  "explanation": "Projekt ma wysoki potencjał...",
  "action_items": [
    "Przygotować dokumentację ESG",
    "Zdefiniować metryki SDG",
    ...
  ],
  "risk_factors": ["Brak znaczących ryzyk"],
  "synergy_opportunities": ["Możliwość rezonatora planetarnego"],
  "disclaimer": "To są rekomendacje analityczne..."
}
```

---

### 5.3 `batch_analyze()` — Analiza portfolio

```python
projects = [
    {
        'name': 'Project A',
        'local_score': 1751.45,
        'pri': 0.92,
        'caf': 0.88,
        'spc': 0.75,
        'domain': 'Education',
    },
    # ... więcej projektów
]

portfolio = analyzer.batch_analyze(projects)

# Słownik zawierający:
# - portfolio_size: int
# - average_gis: float
# - max_gis: float
# - min_gis: float
# - projects_for_global_scale: int
# - all_analyses: List[Dict]
# - projects_recommended_for_scaling: List[str]
```

---

### 5.4 `export_audit_log()` — Eksport dla audytu

```python
filepath = analyzer.export_audit_log("gv_audit.json")

# Plik JSON zawierający:
# {
#   "audit_log": [logowanie zdarzeń],
#   "analysis_history": [wszystkie analizy],
#   "export_timestamp": "..."
# }
```

**Przeznaczenie:** Audyt algorytmiczny, śledzenie decyzji, debugowanie

---

## 6. Przepływ danych

```
[User Input]
    ↓
[calculate_gis()] ← Obliczenie GIS, walidacja
    ↓
[get_recommendation()] ← Rekomendacja strategiczna
    ↓
[Display to User] ← Decyzja pozostaje przy człowieku
    ↓
[batch_analyze() optional] ← Portfolio analysis
    ↓
[export_audit_log()] ← Archiwizacja dla audytu
```

---

## 7. Przykłady użycia

### Przykład 1: Ocena pojedynczego projektu

```python
from CORE.Inference.global_vision_analyzer import GlobalVisionAnalyzer

analyzer = GlobalVisionAnalyzer()

# Krok 1: Obliczenie GIS
metrics = analyzer.calculate_gis(
    local_score=1751.45,
    pri=0.92,
    caf=0.88,
    spc=0.75,
    project_name="Cosmic Education Platform",
    domain="Education",
)

# Krok 2: Generowanie rekomendacji
recommendation = analyzer.get_recommendation(metrics)

# Krok 3: Podejmowanie decyzji przez człowieka
if recommendation['recommendation_level'] == "GLOBAL_SCALE":
    print(f"✅ Rekomendacja: Skalowanie globalne")
    print(f"Kroki: {recommendation['action_items']}")
else:
    print(f"⚠️ Wymaga przeglądu: {recommendation['explanation']}")
```

### Przykład 2: Analiza portfolio

```python
portfolio = [
    {"name": "ProjectA", "local_score": 1800, "pri": 0.95, "caf": 0.92, "spc": 0.90, "domain": "Tech"},
    {"name": "ProjectB", "local_score": 1200, "pri": 0.75, "caf": 0.70, "spc": 0.65, "domain": "Health"},
    {"name": "ProjectC", "local_score": 600, "pri": 0.50, "caf": 0.45, "spc": 0.40, "domain": "Other"},
]

result = analyzer.batch_analyze(portfolio)

print(f"Portfolio Size: {result['portfolio_size']}")
print(f"Average GIS: {result['average_gis']}")
print(f"Projekty do skalowania: {result['projects_recommended_for_scaling']}")
```

### Przykład 3: Integracja z warstwą GOK:AI

```python
# Pseudo-kod integracji

from CORE.Memory.long_term_graph import LongTermGraphManager
from CORE.Inference.global_vision_analyzer import GlobalVisionAnalyzer

# 1. GOK:AI oblicza wynik lokalny
graph_manager = LongTermGraphManager()
local_score = graph_manager.evaluate_project("project_id")

# 2. GlobalVision ocenia wpływ globalny
analyzer = GlobalVisionAnalyzer()
metrics = analyzer.calculate_gis(
    local_score=local_score,
    pri=0.9,  # Z danych o wartościach
    caf=0.85, # Z danych o kierunku
    spc=0.75, # Z danych o synergii
    project_name=project_id,
)

# 3. Rekomendacja dla Drift Money / Apex INFINITY
recommendation = analyzer.get_recommendation(metrics)
if metrics.gis > 8500:
    trigger_drift_money_funding(project_id, recommendation)
    trigger_apex_infinity_narrative(project_id, recommendation)
```

---

## 8. Testy jednostkowe

### Uruchomienie testów

```bash
cd e:\REPO_MASTER_GOKAI\AGI_GOK
python -m pytest tests/test_global_vision.py -v
```

### Pokrycie testów

- ✅ Obliczenie GIS (doskonałe wyniki, zera, mieszane)
- ✅ Normalizacja LocalScore
- ✅ Walidacja wejść (PRI, CAF, SPC w [0, 1])
- ✅ Rekomendacje (GLOBAL_SCALE, HIGH_POTENTIAL, LOCAL_RELEVANCE, REVIEW_NEEDED)
- ✅ Identyfikacja ryzyka
- ✅ Identyfikacja synergii
- ✅ Batch analysis (pojedynczy, wielokrotny projekt)
- ✅ Audit log
- ✅ Integracyjne scenariusze

---

## 9. Bezpieczeństwo i audyt

### Zasady bezpieczeństwa

1. **Przejrzystość:** Wszystkie wagi, progi i wzory są jawne w kodzie
2. **Brak autonomii:** System generuje REKOMENDACJE, nie decyzje
3. **Audytowalność:** Każda analiza jest logowana z timestampem
4. **Offline-first:** System działa w całości lokalnie, bez połączenia z internetem

### Archiwizacja

```python
analyzer.export_audit_log("gv_audit_2026_01_27.json")
# Zawiera:
# - Wszystkie obliczenia
# - Wszystkie ostrzeżenia walidacji
# - Timestampy
# - Metadane projektów
```

---

## 10. Rozszerzanie systemu

### Dodawanie nowych wskaźników

```python
class GlobalVisionAnalyzer:
    # Dodaj nową wagę
    WEIGHT_ENVIRONMENTAL_IMPACT = 0.05  # Nowy wskaźnik
    
    # Przelicz inne wagi (utrzymaj sumę 1.0)
    WEIGHT_PRI = 0.38
    WEIGHT_CAF = 0.33
    WEIGHT_SPC = 0.14
    WEIGHT_LS = 0.10
    
    def calculate_gis(self, ..., environmental_score=0.5):
        # Uwzględnij nowy wskaźnik
        gis_normalized = (
            (pri * self.WEIGHT_PRI) +
            (caf * self.WEIGHT_CAF) +
            (spc * self.WEIGHT_SPC) +
            (normalized_ls * self.WEIGHT_LS) +
            (environmental_score * self.WEIGHT_ENVIRONMENTAL_IMPACT)
        )
        ...
```

### Dodawanie nowych progów

```python
THRESHOLD_IMPACT_CRITICAL = 9500  # Nowy próg
THRESHOLD_IMPACT_URGENT = 9000

def get_recommendation(self, metrics):
    if metrics.gis >= self.THRESHOLD_IMPACT_CRITICAL:
        return "CRITICAL_PLANETARY_IMPACT"
    # ...
```

---

## 11. Troubleshooting

### Błąd: `ValueError: PRI, CAF, SPC muszą być w [0.0, 1.0]`

**Przyczyna:** Wartości wskaźników poza prawidłowym zakresem  
**Rozwiązanie:** Sprawdzić źródło danych, znormalizować do [0, 1]

```python
# Błędnie:
metrics = analyzer.calculate_gis(pri=1.5, caf=0.8, spc=0.7)  # pri poza zakresem

# Poprawnie:
metrics = analyzer.calculate_gis(pri=0.85, caf=0.8, spc=0.7)
```

### Błąd: `KeyError: 'local_score' w batch_analyze`

**Przyczyna:** Brakuje wymaganego pola w słowniku projektu  
**Rozwiązanie:** Upewnij się, że każdy projekt ma wszystkie pola:

```python
# Błędnie:
projects = [{"name": "P1", "pri": 0.9}]  # Brakuje local_score, caf, spc

# Poprawnie:
projects = [{
    "name": "P1",
    "local_score": 1500.0,
    "pri": 0.9,
    "caf": 0.85,
    "spc": 0.75,
    "domain": "Tech",
}]
```

---

## 12. Performans i skalowanie

### Wydajność

| Operacja | Czas | Skalowalność |
| :--- | :---: | :--- |
| `calculate_gis()` | < 1 ms | O(1) |
| `get_recommendation()` | < 5 ms | O(1) |
| `batch_analyze(N)` | N × 1.5 ms | O(N) |
| `export_audit_log()` | < 50 ms | O(N) — liniowe z liczbą analiz |

### Pamięć

- Historia analiz: ~500 B / analiza
- Audit log: ~200 B / wpis
- Dla 1000 analiz: ~700 KB

---

## 13. Przyszłe rozszerzenia

- [ ] Integracja z rzeczywistymi danymi ESG/SDG
- [ ] Machine Learning do predykcji PRI/CAF na podstawie opisu projektu
- [ ] Integracja z Drift Money i Apex INFINITY (webhook)
- [ ] GUI dla wizualizacji Impact Maps
- [ ] Multi-language support

---

## 14. Kontakt i wsparcie

**Autor:** Patryk Sobierański (META-GENIUSZ®️)  
**Kontakt:** GitHub Issues w repozytorium AGI_GOK  
**Licencja:** Apache 2.0

---

**Koniec przewodnika technicznego.**
