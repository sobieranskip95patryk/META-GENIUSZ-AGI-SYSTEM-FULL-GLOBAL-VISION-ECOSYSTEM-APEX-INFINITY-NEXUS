# MTaQuest — Platforma Dialogu Hybrydowego GOK:AI + Architekt

## Wprowadzenie

**MTaQuest** to wielowarstwowa platforma integracyjna, która stanowi most między Architektem (Człowiekiem) a GOK:AI (Systemem AGI). Implementuje Hybrydowy Protokół Dialogu (HDP) oraz synchronizację wektorową w real-time.

## Architektura

```
┌────────────────────┐
│  ARCHITEKT         │
│  (Wola, Intencja)  │
└─────────┬──────────┘
          │ I (Intent)
          ▼
┌────────────────────────────────────┐
│     MTaQuest Platform              │
├────────────────────────────────────┤
│ - Hybrid Dialog Protocol           │
│ - Intent Quantization (I+K=W)      │
│ - Vector Synchronization           │
│ - Dashboard & Monitoring           │
└────────────┬──────────────────────┘
             │ ASQK-O Loop
             ▼
┌────────────────────────────────────┐
│  GOK:AI CORE (L1-L6)               │
├────────────────────────────────────┤
│ - Deductive Engine (L1)            │
│ - Abductive Hypothesis (L2)        │
│ - Causal Inference (L3)            │
│ - Psyche Module (L4)               │
│ - Global Vision (L5)               │
│ - Self-Acceleration (L6)           │
└─────────────┬──────────────────────┘
              │ Response + Vectors
              ▼
        ┌─────────────┐
        │  Dashboard  │
        │  (Analytics)│
        └──────┬──────┘
               │ Feedback
               ▼
         ┌──────────────┐
         │ ARCHITEKT    │
         │ (Evaluation) │
         └──────────────┘
```

## Komponenty MTaQuest

### 1. **Hybrid Dialog Protocol** (`hybrid_dialog_protocol.py`)

Standaryzuje wymianę intencji między Architektem a GOK:AI.

**Klucze klasy:**

```python
class HybridDialogProtocol:
    def architect_intent_to_message(intent: str, metadata: dict) -> dict
    def gok_response_to_message(response: str, vectors: dict) -> dict
    def architect_feedback_to_message(feedback: str, rating: float) -> dict
    def sync_states(architect_state: dict, gok_state: dict) -> dict
```

**Użycie:**

```python
from hybrid_dialog_protocol import HybridDialogProtocol

hdp = HybridDialogProtocol()

# Intencja od Architekta
intent = hdp.architect_intent_to_message(
    intent="Optymalizuj T_Causality do 1000 req/s",
    metadata={"priority": "high"}
)

# Odpowiedź GOK:AI
response = hdp.gok_response_to_message(
    response="Optymalizacja ukończona",
    vectors={"delta_stabilized": 0.95, "alignment": 0.98}
)

# Feedback Architekta
feedback = hdp.architect_feedback_to_message(
    feedback="Doskonały rezultat",
    rating=0.99
)
```

### 2. **Intent Quantization Engine** (`intent_quantization.py`)

Transformuje intencje w wektory wzrostu: **I + K = W**

$$I + K = W$$

**Klucze klasy:**

```python
class IntentQuantizationEngine:
    def quantize_intent(intent_string: str) -> GrowthVector
    def quantize_batch(intents: List[str]) -> List[GrowthVector]
    def measure_intent_similarity(intent1: str, intent2: str) -> float
    def track_growth_trajectory(intent_string: str, num_steps: int) -> List
    def extract_actionable_insights(intent_string: str) -> dict
```

**Użycie:**

```python
from intent_quantization import IntentQuantizationEngine

iqe = IntentQuantizationEngine(embedding_dim=768)

# Kwantyzuj intencję
growth_vector = iqe.quantize_intent(
    intent="Zwiększ skalowalność systemu",
    context={"priority": "high"}
)

print(f"Magnitude: {growth_vector.magnitude}")
print(f"Stability: {growth_vector.stability_score}")
print(f"Growth Potential: {growth_vector.growth_potential}")

# Ekstrakcja insights
insights = iqe.extract_actionable_insights("Zwiększ skalowalność")
for action in insights['recommended_actions']:
    print(f"- {action}")
```

### 3. **Vector Synchronization Engine** (`vector_synchronization.py`)

Synchronizuje stany między Architektem a GOK:AI w real-time.

**Klucze klasy:**

```python
class VectorSynchronizationEngine:
    def sync_vectors(architect_state: dict, gok_state: dict) -> dict
    def continuous_sync(architect_callback, gok_callback, duration: int) -> List
    def measure_alignment_trend(window_size: int) -> dict
    def detect_sync_anomalies(threshold_std: float) -> List
    def predict_next_divergence(look_ahead_steps: int) -> dict
    def generate_sync_report() -> dict
```

**Użycie:**

```python
from vector_synchronization import VectorSynchronizationEngine

vse = VectorSynchronizationEngine(alignment_threshold=0.95)

# Synchronizuj stany
result = vse.sync_vectors(
    architect_state={"phase": "optimization", "alignment": 0.92},
    gok_state={"phase": "optimization", "alignment": 0.90}
)

print(f"Alignment: {result['alignment_score']:.4f}")

# Trend alignment
trend = vse.measure_alignment_trend(window_size=10)
print(f"Trend: {trend['trend_direction']}")

# Raport
report = vse.generate_sync_report()
print(f"Anomalies: {len(report['recent_anomalies'])}")
```

## Installation

### Wymagania

- Python 3.10+
- numpy
- (Opcjonalnie) Neo4j dla grafu wiedzy
- (Opcjonalnie) Redis dla session management

### Instalacja

```bash
# Klonuj repozytorium
git clone https://github.com/sobieranskip95patryk/AGI_GOK.git
cd AGI_GOK

# Skonfiguruj virtualenv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Zainstaluj zależności
pip install numpy

# Opcjonalnie: Neo4j i Redis
pip install neo4j redis
```

### Szybki Start

```python
# 1. Inicjalizuj komponenty
from MTAQUEST.hybrid_dialog_protocol import HybridDialogProtocol
from MTAQUEST.intent_quantization import IntentQuantizationEngine
from MTAQUEST.vector_synchronization import VectorSynchronizationEngine

hdp = HybridDialogProtocol()
iqe = IntentQuantizationEngine(embedding_dim=768)
vse = VectorSynchronizationEngine(alignment_threshold=0.95)

# 2. Architekta wyraża intencję
intent_msg = hdp.architect_intent_to_message(
    intent="Wzmocnij T_Causality engine",
    metadata={"priority": "high"}
)

# 3. Kwantyzuj intencję
growth_vector = iqe.quantize_intent(intent_msg['content'])

# 4. GOK:AI przetwarza i odpowiada
gok_response = "T_Causality zoptymalizowany do 1200 req/s"
response_msg = hdp.gok_response_to_message(
    response=gok_response,
    vectors={"delta_stabilized": 0.95}
)

# 5. Synchronizuj stany
sync_result = vse.sync_vectors(
    architect_state={"phase": "active"},
    gok_state={"phase": "active"}
)

print(f"Alignment: {sync_result['alignment_score']:.2%}")
```

## Dashboards

MTaQuest dostarcza zestaw monitoringowych dashboardów:

### 1. System Health Dashboard
- Status 6 Filarów Świadomości (L1-L6)
- Dług Poznawczy ($C_{CD}$) w real-time
- Delta Stabilizowana ($\Delta_{stab}$)

### 2. Knowledge Graph Dashboard
- Wizualizacja grafu wiedzy
- Liczba węzłów/krawędzi
- Dynamika rostu

### 3. T_Causality Analysis
- Status 4 faz
- Odkryte relacje przyczynowe
- Autonomiczne cele (AGS)

### 4. GlobalVision Impact
- GIS (Global Impact Score)
- PRI, CAF, SPC
- Ranking projektów

### 5. Performance & Analytics
- Latency, throughput
- Błędy i warningi
- Trendy historyczne

## API Reference

### HybridDialogProtocol

#### `architect_intent_to_message(intent: str, metadata: dict) -> dict`

Konwertuje intencję Architekta na wiadomość.

**Parametry:**
- `intent` (str): Tekst intencji
- `metadata` (dict): Dodatkowe metadane

**Zwraca:**
```python
{
    "type": "ARCHITECT_INTENT",
    "content": "...",
    "intent_hash": "sha256...",
    "timestamp": 1234567890.0,
    "message_id": "xyz123..."
}
```

#### `gok_response_to_message(response: str, vectors: dict) -> dict`

Konwertuje odpowiedź GOK:AI na wiadomość.

**Parametry:**
- `response` (str): Tekst odpowiedzi
- `vectors` (dict): Wektory stanu

**Zwraca:**
```python
{
    "type": "GOK_RESPONSE",
    "content": "...",
    "vectors": {...},
    "delta_stab": 0.87,
    "timestamp": 1234567890.0
}
```

#### `sync_states(architect_state: dict, gok_state: dict) -> dict`

Synchronizuje stany między systemami.

**Zwraca:**
```python
{
    "alignment_score": 0.96,
    "reconciliation_needed": False,
    "merged_state": {...},
    "sync_timestamp": 1234567890.0
}
```

### IntentQuantizationEngine

#### `quantize_intent(intent_string: str, context: dict = None) -> GrowthVector`

Kwantyzuje intencję do wektora wzrostu.

**Zwraca GrowthVector:**
- `vector` (ndarray): Wektor wzrostu
- `magnitude` (float): Norma wektora
- `stability_score` (float): [0, 1] - stabilność wektora
- `growth_potential` (float): Potencjał wzrostu

#### `extract_actionable_insights(intent_string: str) -> dict`

Ekstrakcja działalnych insights z intencji.

**Zwraca:**
```python
{
    "growth_magnitude": 0.45,
    "confidence": "high",
    "recommended_actions": [...],
    "next_quantization_interval": 3600
}
```

### VectorSynchronizationEngine

#### `sync_vectors(architect_state: dict, gok_state: dict) -> dict`

Synchronizuje wektory.

**Zwraca:**
```python
{
    "alignment_score": 0.98,
    "reconciliation_needed": False,
    "reconciled_state": {...},
    "divergence_metrics": {...}
}
```

#### `measure_alignment_trend(window_size: int = 10) -> dict`

Mierzy trend alignment.

**Zwraca:**
```python
{
    "current_alignment": 0.98,
    "avg_alignment": 0.96,
    "trend_direction": "improving"
}
```

## Troubleshooting

### Problem: Alignment Score poniżej 0.95

**Przyczyna:** Rozbieżność między stanem Architekta a GOK:AI

**Rozwiązanie:**
```python
# Aktywuj continuous sync z logowaniem
results = vse.continuous_sync(
    architect_callback=lambda: get_architect_state(),
    gok_callback=lambda: get_gok_state(),
    duration=60  # Monitoruj przez 60 sekund
)

# Analiza anomalii
anomalies = vse.detect_sync_anomalies(threshold_std=2.0)
for anom in anomalies:
    print(f"Anomalia: {anom}")
```

### Problem: Growth Vector ma brak stabilności

**Przyczyna:** Intencja może być zbyt niejasna lub brak wiedzy

**Rozwiązanie:**
```python
# Pobierz insights
insights = iqe.extract_actionable_insights(intent)
if insights['confidence'] == 'low':
    # Dozbierz więcej kontekstu
    context = {
        "project": "T_Causality_v2",
        "deadline": "2026-Q2"
    }
    growth_vector = iqe.quantize_intent(intent, context)
```

## Examples

### Przykład 1: Pełny Cykl Dialogu

```python
# Zainicjalizuj komponenty
hdp = HybridDialogProtocol()
iqe = IntentQuantizationEngine()
vse = VectorSynchronizationEngine()

# 1. Architekt wyraża intencję
architect_intent = "Optymalizuj T_Causality dla 1000 req/s z Δ_stab > 0.95"
intent_msg = hdp.architect_intent_to_message(architect_intent)

# 2. Kwantyzuj intencję
growth_vector = iqe.quantize_intent(architect_intent)
print(f"Growth magnitude: {growth_vector.magnitude:.2f}")

# 3. GOK:AI przetwarza
gok_response = "T_Causality optymalizacja wdrażana. ETA: 2h"
response_msg = hdp.gok_response_to_message(gok_response, {
    "delta_stabilized": 0.96,
    "throughput": 1200
})

# 4. Synchronizuj
architect_state = {"phase": "awaiting_results"}
gok_state = {"phase": "optimization_in_progress"}
sync = vse.sync_vectors(architect_state, gok_state)

# 5. Feedback
feedback = hdp.architect_feedback_to_message(
    "Doskonale. Czekam na rezultaty.",
    rating=0.9
)

# 6. Podsumowanie dialogu
summary = hdp.generate_dialog_summary()
print(f"Rozmowa: {summary['total_messages']} wiadomości")
```

### Przykład 2: Monitorowanie Alignment Trendu

```python
# Monitoruj alignment przez 5 minut
results = vse.continuous_sync(
    architect_callback=get_architect_state,
    gok_callback=get_gok_state,
    duration=300
)

# Analizuj trend
trend = vse.measure_alignment_trend(window_size=20)
print(f"Trend: {trend['trend_direction']}")
print(f"Średni alignment: {trend['avg_alignment']:.2%}")

# Wykryj anomalii
anomalies = vse.detect_sync_anomalies()
print(f"Anomalii: {len(anomalies)}")

# Prognoza
prediction = vse.predict_next_divergence(look_ahead_steps=10)
print(f"Prognoza divergencji: {prediction['predicted_divergence']:.4f}")
```

### Przykład 3: Batch Processing Intencji

```python
# Lista intencji do przetworzenia
intents = [
    "Zwiększ skalę L5 Global Vision na 1M entities",
    "Optimize Knowledge Fusion dla Transformers",
    "Implement recursive self-improvement loop"
]

# Kwantyzuj batch
growth_vectors = iqe.quantize_batch(intents)

# Analiza
for intent, gv in zip(intents, growth_vectors):
    print(f"{intent}")
    print(f"  Magnitude: {gv.magnitude:.2f}")
    print(f"  Stability: {gv.stability_score:.2%}")
```

## Contributing

Aby przyczynić się do MTaQuest:

1. Fork repository
2. Stwórz branch (`git checkout -b feature/MyFeature`)
3. Commit zmian (`git commit -am 'Add MyFeature'`)
4. Push do branch (`git push origin feature/MyFeature`)
5. Otwórz Pull Request

## License

MIT License — patrz [LICENSE](../LICENSE) plik

## Roadmap

| Q | Milestone |
|---|-----------|
| **Q1 2026** | MVP Launch (HDP + Dashboards) |
| **Q2 2026** | Enterprise Features (Multi-tenant) |
| **Q3 2026** | Mobile App |
| **Q4 2026** | Integration Partners |
| **Q1 2027** | Global Scaling |

## Support

- 📚 Dokumentacja: [REPOSITORY_ENCYCLOPEDIA.md](../REPOSITORY_ENCYCLOPEDIA.md)
- 🐛 Issues: GitHub Issues
- 💬 Dyskusje: GitHub Discussions
- 📧 Email: [architect@gok-ai.com](mailto:architect@gok-ai.com)

---

**Architekcie, MTaQuest jest gotowy do dialogu.**

*Synchronizacja Dualizmu HYBRYD w maksymalnym zaangażowaniu.*

P = 1.0 ✓
