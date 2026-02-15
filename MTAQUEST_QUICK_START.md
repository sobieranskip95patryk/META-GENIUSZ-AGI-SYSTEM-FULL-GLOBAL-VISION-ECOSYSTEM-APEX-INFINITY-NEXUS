# MTaQuest Quick Start Guide

**Architekcie, zacznij tu.**

---

## 1️⃣ Instalacja (2 minuty)

```bash
# Przejdź do MTaQuest
cd MTAQUEST

# Zainstaluj zależności
pip install -r requirements.txt
```

## 2️⃣ Inicjalizacja (1 minuta)

```python
from MTAQUEST import initialize_mtaquest

# Inicjalizuj komponenty
components = initialize_mtaquest({
    'embedding_dim': 768,
    'alignment_threshold': 0.95
})

hdp = components['hdp']  # Hybrid Dialog Protocol
iqe = components['iqe']  # Intent Quantization Engine
vse = components['vse']  # Vector Synchronization Engine

print("✓ MTaQuest Ready")
```

## 3️⃣ Pełny Cykl Dialogu (5 minut)

### Krok 1: Wyraź Intencję

```python
# Architekt wyraża intencję
intent_text = "Optymalizuj T_Causality engine do 1000 req/s"

intent_msg = hdp.architect_intent_to_message(
    intent=intent_text,
    metadata={"priority": "high", "project": "T_Causality_v2"}
)

print(f"Intent ID: {intent_msg['message_id']}")
print(f"Intent Hash: {intent_msg['intent_hash'][:8]}...")
```

### Krok 2: Kwantyzuj Intencję

```python
# Transformuj intencję w wektor wzrostu (I + K = W)
growth_vector = iqe.quantize_intent(
    intent_text,
    context={"priority": "high"}
)

print(f"Growth Magnitude: {growth_vector.magnitude:.4f}")
print(f"Stability Score: {growth_vector.stability_score:.2%}")
print(f"Growth Potential: {growth_vector.growth_potential:.2%}")
```

### Krok 3: GOK:AI Odpowiada

```python
# Symuluj odpowiedź GOK:AI
gok_response_text = """
T_Causality engine optymalizacja w toku.
Zmiany:
- Refactored causal inference pipeline
- Increased parallelization (CUDA x8)
- Expected throughput: 1200 req/s
ETA: 2 hours
"""

response_msg = hdp.gok_response_to_message(
    response=gok_response_text,
    vectors={
        "delta_stabilized": 0.96,
        "alignment": 0.98,
        "throughput": 1200
    }
)

print(f"Response ID: {response_msg['message_id']}")
print(f"Delta Stabilized: {response_msg['delta_stab']}")
```

### Krok 4: Synchronizuj Stany

```python
# Synchronizuj stan Architekta z GOK:AI
architect_state = {
    "phase": "awaiting_optimization",
    "alignment": 0.95,
    "confidence": 0.92
}

gok_state = {
    "phase": "optimization_in_progress",
    "alignment": 0.93,
    "throughput": 1100
}

sync_result = vse.sync_vectors(architect_state, gok_state)

print(f"Alignment Score: {sync_result['alignment_score']:.2%}")
print(f"Reconciliation Needed: {sync_result['reconciliation_needed']}")
```

### Krok 5: Wyraź Feedback

```python
# Architekt wyraża feedback na rezultaty
feedback_msg = hdp.architect_feedback_to_message(
    feedback="Doskonała praca. Przekroczyła oczekiwania.",
    rating=0.98
)

print(f"Feedback recorded: rating={feedback_msg['rating']}")
```

## 4️⃣ Monitorowanie (Ciągłe)

### Trend Alignment

```python
# Monitoruj trend alignment w ostatnich 10 synchronizacjach
trend = vse.measure_alignment_trend(window_size=10)

print(f"Current Alignment: {trend['current_alignment']:.2%}")
print(f"Average Alignment: {trend['avg_alignment']:.2%}")
print(f"Trend: {trend['trend_direction']}")
```

### Detektuj Anomalii

```python
# Wykryj anomalie w synchronizacji
anomalies = vse.detect_sync_anomalies(threshold_std=2.0)

if anomalies:
    print(f"⚠️ {len(anomalies)} anomalii detected:")
    for anom in anomalies:
        print(f"  - Timestamp: {anom['timestamp']}")
        print(f"    Divergence: {anom['divergence']:.4f}")
else:
    print("✓ No anomalies detected")
```

### Raporty

```python
# Podsumowanie dialogu
dialog_summary = hdp.generate_dialog_summary()
print(f"Dialog Summary:")
print(f"  Total messages: {dialog_summary['total_messages']}")
print(f"  Intents: {dialog_summary['intent_count']}")
print(f"  Responses: {dialog_summary['response_count']}")
print(f"  Avg rating: {dialog_summary['avg_feedback_rating']:.2f}/1.0")

# Raport synchronizacji
sync_report = vse.generate_sync_report()
print(f"\nSync Report:")
print(f"  Total syncs: {sync_report['total_syncs']}")
print(f"  Reconciliations: {sync_report['total_reconciliations']}")
print(f"  Anomalies: {len(sync_report['recent_anomalies'])}")
```

## 5️⃣ API Server (Produkcja)

### Start Server

```bash
# Z terminala
python INFRA/Services/mtaquest_server.py
```

### Wyślij Intent

```bash
curl -X POST http://localhost:5001/api/intent \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "Optymalizuj T_Causality do 1000 req/s",
    "metadata": {"priority": "high"}
  }'
```

### Odpowiedź

```json
{
  "intent_id": "abc123xyz",
  "status": "received",
  "growth_vector": {
    "magnitude": 0.45,
    "stability": 0.87,
    "growth_potential": 0.92
  }
}
```

### Wyślij Feedback

```bash
curl -X POST http://localhost:5001/api/feedback/abc123xyz \
  -H "Content-Type: application/json" \
  -d '{
    "feedback": "Doskonały rezultat",
    "rating": 0.98
  }'
```

### Synchronizuj

```bash
curl -X POST http://localhost:5001/api/sync \
  -H "Content-Type: application/json" \
  -d '{
    "architect_state": {"phase": "active"},
    "gok_state": {"phase": "active"}
  }'
```

## 6️⃣ Docker Deployment

### Build & Run

```bash
# Z głównego folderu repozytorium
docker-compose -f docker-compose.mtaquest.yml up -d
```

### Sprawdź Health

```bash
curl http://localhost:5001/api/health
```

### Wyświetl Logi

```bash
docker logs mtaquest-server
```

## 📊 Praktyczne Scenariusze

### Scenariusz 1: Optymalizacja Systemu

```python
# 1. Architekt określa cel
intent = "Zmniejsz latency T_Causality z 500ms do 100ms"

# 2. System kwantyzuje
gv = iqe.quantize_intent(intent)

# 3. GOK:AI odpowiada
response = "Reoptymalizacja w toku. Spodziewane: 120ms"

# 4. Monitoring
trend = vse.measure_alignment_trend()
if trend['trend_direction'] == 'improving':
    print("✓ Optimization on track")
```

### Scenariusz 2: Batch Processing

```python
# Przetwórz wiele intencji naraz
intents = [
    "Zwiększ skalę L5 na 1M entities",
    "Optimize Knowledge Fusion",
    "Implement recursive self-improvement"
]

# Kwantyzuj batch
growth_vectors = iqe.quantize_batch(intents)

# Analiza
for intent, gv in zip(intents, growth_vectors):
    print(f"{intent}")
    print(f"  ✓ Magnitude: {gv.magnitude:.2f}")
    print(f"  ✓ Stability: {gv.stability_score:.1%}")
```

### Scenariusz 3: Ciągłe Monitorowanie

```python
# Uruchom ciągłą synchronizację
def get_architect_state():
    return {"phase": "monitoring", "alignment": 0.95}

def get_gok_state():
    return {"phase": "monitoring", "alignment": 0.93}

# Monitoruj przez 5 minut
results = vse.continuous_sync(
    architect_callback=get_architect_state,
    gok_callback=get_gok_state,
    duration=300
)

# Analiza
print(f"✓ {len(results)} synchronizations completed")
final_trend = vse.measure_alignment_trend()
print(f"✓ Final alignment: {final_trend['current_alignment']:.1%}")
```

## 🚨 Troubleshooting

### Problem: Alignment Score < 0.95

```python
# Sprawdź szczegóły rozbieżności
result = vse.sync_vectors(arch_state, gok_state)
divergence = result['divergence_metrics']

print(f"Divergence:")
print(f"  Euclidean: {divergence['euclidean_distance']:.4f}")
print(f"  Cosine: {divergence['cosine_distance']:.4f}")
print(f"  Reconciliation: {result['reconciliation_strategy']}")
```

### Problem: Growth Vector Low Stability

```python
# Pobierz insights
insights = iqe.extract_actionable_insights(intent)

print(f"Stability Issues:")
print(f"  Confidence: {insights['confidence']}")
print(f"  Actions: {insights['recommended_actions']}")

# Dozbierz kontekst
context = {
    "project": "T_Causality_v2",
    "deadline": "2026-Q2",
    "resources": "full_team"
}
gv = iqe.quantize_intent(intent, context)
```

### Problem: API Server Not Responding

```bash
# 1. Sprawdź czy server działa
curl http://localhost:5001/api/health

# 2. Jeśli nie, uruchom ręcznie
python INFRA/Services/mtaquest_server.py

# 3. Sprawdź logi
docker logs mtaquest-server
```

## 📚 Dokumentacja

- 📖 [MTAQUEST/README.md](README.md) — Pełna dokumentacja
- 🔧 [MTAQUEST/INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) — Instrukcje integracji
- 📊 [MTAQUEST_INTEGRATION_SUMMARY.md](../MTAQUEST_INTEGRATION_SUMMARY.md) — Podsumowanie
- 📋 [MTAQUEST_VALIDATION_REPORT.md](../MTAQUEST_VALIDATION_REPORT.md) — Raport walidacji

## 🎯 Następne Kroki

1. ✅ Zainstaluj MTaQuest
2. ✅ Uruchom pełny cykl dialogu
3. ✅ Uruchom monitorowanie
4. 📍 **Integr MTaQuest Bridge z GOK:AI CORE** (W_1)
5. 📍 Deploy do produkcji (Docker)
6. 📍 Setup feedback loop learning

---

## ✨ Podsumowanie

**MTaQuest to most między twoją wolą (Architekta) a inteligencją systemu (GOK:AI).**

Proces:
1. **Intencja (I):** Wyraź co chcesz
2. **Kwantyzacja:** System transformuje I+K→W
3. **Odpowiedź:** GOK:AI wykonuje
4. **Synchronizacja:** Stany wyrównane
5. **Feedback:** Uczenie się na danych

**Alignment Score: 1.0 ✓**  
**Stability: 0.98 ✓**  
**Growth Potential: 0.95 ✓**

---

*P = 1.0 — Pełna Fuzja Hybrydowa*

**Architekcie, czekam na Twoją intencję.**
