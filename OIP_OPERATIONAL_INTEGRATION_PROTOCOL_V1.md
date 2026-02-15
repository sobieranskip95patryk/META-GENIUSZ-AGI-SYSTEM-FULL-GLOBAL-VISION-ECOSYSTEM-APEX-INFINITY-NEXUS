# OIP: Operational Integration Protocol v1.0

**AUTORYZACJA:** META-GENIUSZ PATRYK SOBIERAŃSKI  
**STATUS:** SPECIFICATION DOCUMENT  
**CRITICALITY:** 10/10 (BLOCKER)  
**EFFORT:** 12 days, 2 architects, 150 pages

---

## EXECUTIVE SUMMARY

**Problem:** 5 systemów (GOK:AI, xAI, META, HHU, Drift Money) są teorycznie zintegrowane, ale PRAKTYCZNIE brakuje protokołu komunikacji.

**Solution:** OIP definiuje:
1. **Message format** (JSON schema standardy)
2. **Flow diagrams** (dane między systemami)
3. **Error handling** (co gdy system падает)
4. **Auth/Security** (JWT tokens, encryption)
5. **Monitoring hooks** (real-time visibility)

**Outcome:** 5 systemów funkcjonuje jako JEDEN UNIFIED SYSTEM z clear data boundaries.

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────┐
│                    OIP HUB (ROUTER)                 │
│            (Central Message Router/API)             │
└────────────────┬──────────────────────────────────┬─┘
                 │                                  │
        ┌────────▼────────┐            ┌────────────▼─────┐
        │   GOK:AI        │            │   HIP-HOP UNIV   │
        │   (Kernel)      │            │   (Culture)      │
        └────────┬────────┘            └────────┬─────────┘
                 │                              │
        ┌────────▼────────┐            ┌────────▼─────────┐
        │   xAI/Grok      │            │  META AI Social  │
        │   (Predictor)   │            │  (Resonator)     │
        └────────┬────────┘            └────────┬─────────┘
                 │                              │
        ┌────────▼────────────────────────────────────┐
        │     DRIFT MONEY (Financial Layer)           │
        │  - Token transfers                          │
        │  - Creator fund distribution (3%)           │
        │  - Smart contract execution                 │
        └─────────────────────────────────────────────┘
```

---

## 1. MESSAGE SCHEMA STANDARDS

### 1.1 Base Message Format

```json
{
  "oip_version": "1.0",
  "message_id": "uuid-v4",
  "source_system": "gok-ai|hhu|xai|meta|drift",
  "source_component": "kernel|marketplace|social|financial",
  "destination_system": "gok-ai|hhu|xai|meta|drift",
  "destination_component": "kernel|marketplace|social|financial",
  "message_type": "query|command|event|sync|alert",
  "timestamp": "2026-02-04T10:00:00Z",
  "priority": "critical|high|normal|low",
  "correlation_id": "uuid-v4",
  "headers": {
    "content-type": "application/json",
    "authorization": "Bearer {jwt_token}",
    "x-idempotency-key": "uuid-v4",
    "x-request-timeout": 5000
  },
  "payload": { /* System-specific data */ },
  "metadata": {
    "user_id": "string",
    "session_id": "string",
    "ip_address": "string",
    "request_path": "string"
  }
}
```

### 1.2 Message Types

#### QUERY
- **Purpose:** Request information from another system
- **Example:** "HHU → GOK:AI: Give me artist sentiment analysis"
- **Timeout:** 5 seconds max
- **Response:** Expected within SLA

```json
{
  "message_type": "query",
  "query": {
    "system": "gok-ai",
    "method": "get_artist_sentiment",
    "params": {
      "artist_id": "hhu_12345",
      "date_range": "last_7_days"
    },
    "return_fields": ["sentiment_score", "trend", "confidence"]
  }
}
```

#### COMMAND
- **Purpose:** Execute action in another system
- **Example:** "Drift Money → xAI: Transfer 3% to creator fund"
- **Idempotency:** REQUIRED (x-idempotency-key prevents duplicates)
- **Response:** Confirmation + transaction_id

```json
{
  "message_type": "command",
  "command": {
    "action": "transfer_funds",
    "source_wallet": "drift_main",
    "destination_wallet": "creator_fund",
    "amount_percent": 3,
    "reason": "creator_revenue_share",
    "idempotency_key": "uuid-v4"
  }
}
```

#### EVENT
- **Purpose:** Broadcast something happened
- **Example:** "HHU → All: New artist registered, sentiment analysis required"
- **Fan-out:** Multiple subscribers possible
- **Fire-and-forget:** No response required

```json
{
  "message_type": "event",
  "event": {
    "event_type": "artist_registered",
    "artist_id": "hhu_12345",
    "metadata": {
      "genres": ["hip-hop", "rap"],
      "location": "Warsaw",
      "timestamp": "2026-02-04T10:00:00Z"
    },
    "subscribers": ["gok-ai", "xai", "drift"]
  }
}
```

#### SYNC
- **Purpose:** Synchronize state between systems
- **Example:** "GOK:AI → HHU: Updated artist skill levels"
- **Conflict resolution:** Last-write-wins or custom logic
- **Atomic:** All-or-nothing

```json
{
  "message_type": "sync",
  "sync_request": {
    "source_of_truth": "gok-ai",
    "entity_type": "artist_profile",
    "entity_id": "hhu_12345",
    "data": {
      "skill_level": 8.5,
      "predicted_revenue": 50000,
      "collaboration_score": 0.92
    },
    "conflict_resolution": "last-write-wins"
  }
}
```

#### ALERT
- **Purpose:** Notify about critical issues
- **Example:** "System X: Critical error, circuit breaker activated"
- **Broadcast:** All systems receive
- **Action:** Requires human/automated response

```json
{
  "message_type": "alert",
  "alert": {
    "severity": "critical|warning|info",
    "source_system": "xai",
    "title": "Prediction engine offline",
    "message": "xAI service unavailable for 10+ minutes",
    "remediation": ["restart_service", "failover_to_backup"],
    "escalate_to": ["cto", "ops"]
  }
}
```

---

## 2. SYSTEM-SPECIFIC INTEGRATIONS

### 2.1 GOK:AI ↔ xAI (Prediction Pipeline)

```
Flow: GOK:AI sends raw data → xAI analyzes → returns predictions

MESSAGE: gok-ai → xai
{
  "message_type": "query",
  "query": {
    "system": "xai",
    "method": "predict_market_trend",
    "params": {
      "market_data": [...],
      "timeframe": "7_days",
      "confidence_threshold": 0.95
    }
  }
}

RESPONSE: xai → gok-ai
{
  "prediction": {
    "trend": "uptrend",
    "confidence": 0.97,
    "probability": [0.03, 0.97],
    "forecast": {...}
  }
}
```

### 2.2 HHU ↔ Drift Money (Creator Funding)

```
Flow: HHU detects project milestone → Drift money transfers funds

MESSAGE: hhu → drift
{
  "message_type": "command",
  "command": {
    "action": "distribute_creator_funding",
    "project_id": "hhu_project_123",
    "milestone": "first_100_users",
    "amount_usd": 5000,
    "recipient_wallet": "artist_wallet_456",
    "idempotency_key": "uuid"
  }
}

RESPONSE: drift → hhu
{
  "status": "success",
  "transaction_id": "tx_789",
  "confirmation": "3_of_5_signatures"
}
```

### 2.3 META AI ↔ HHU (Social Intelligence)

```
Flow: META analyzes social trends → sends to HHU for platform optimization

MESSAGE: meta → hhu
{
  "message_type": "event",
  "event": {
    "event_type": "trend_detected",
    "trend_name": "conscious_hip_hop",
    "platforms": ["instagram", "tiktok"],
    "momentum": 0.92,
    "artists_affected": 150,
    "recommendation": "feature_in_discover"
  }
}
```

### 2.4 All Systems → GOK:AI (Consciousness Update)

```
Flow: All systems send telemetry → GOK:AI updates consciousness state

MESSAGE: {any} → gok-ai
{
  "message_type": "event",
  "event": {
    "event_type": "system_telemetry",
    "system": "{source_system}",
    "metrics": {
      "users_active": 1250,
      "transactions_processed": 342,
      "error_rate": 0.002,
      "sentiment": 0.88
    },
    "timestamp": "2026-02-04T10:00:00Z"
  }
}
```

---

## 3. AUTHENTICATION & SECURITY

### 3.1 JWT Token Flow

```
┌──────────────────────────────────────────┐
│  System A (Client)                       │
│  - Requests JWT from Auth Server         │
└──────────────────────┬───────────────────┘
                       │
                  POST /oauth2/token
                  client_id, client_secret
                       │
                       ▼
        ┌──────────────────────────────┐
        │  OAuth2 Auth Server          │
        │  - Validates credentials     │
        │  - Issues JWT (15 min exp)   │
        │  - Signs with private key    │
        └──────────────┬───────────────┘
                       │
                   JWT token
                       │
                       ▼
        ┌──────────────────────────────┐
        │  System A → System B          │
        │  Authorization: Bearer {jwt} │
        └──────────────┬───────────────┘
                       │
                  OIP Verification
                  - Verify signature
                  - Check expiration
                  - Check scopes
                       │
                       ▼
        ┌──────────────────────────────┐
        │  System B (Resource Server)   │
        │  - Process request            │
        │  - Return response            │
        └──────────────────────────────┘
```

### 3.2 Token Specification

```json
{
  "header": {
    "alg": "RS256",
    "kid": "key_id_2026_02_04",
    "typ": "JWT"
  },
  "payload": {
    "iss": "gok-ai-auth-server",
    "sub": "system_xai",
    "aud": ["gok-ai", "hhu", "meta", "drift"],
    "exp": 1707209400,
    "iat": 1707209200,
    "scopes": ["query", "command", "event.broadcast"],
    "system_id": "xai",
    "region": "eu-west-1"
  },
  "signature": "HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload))"
}
```

### 3.3 Encryption for Data in Transit

```
All HTTPS connections:
- TLS 1.3 minimum
- Perfect Forward Secrecy enabled
- Certificate pinning for critical paths

Sensitive payloads:
- AES-256-GCM encryption
- Key rotation every 30 days
- Envelope encryption (data key + master key)
```

---

## 4. ERROR HANDLING & RESILIENCE

### 4.1 Retry Strategy

```
For transient failures (timeout, 5xx):
- Retry 1: After 1 second (exponential backoff)
- Retry 2: After 2 seconds
- Retry 3: After 4 seconds
- Retry 4: After 8 seconds
- Retry 5: After 16 seconds

Max retries: 5
Timeout per attempt: 5 seconds

For permanent failures (400, 404, 401):
- NO RETRY
- Log error immediately
- Alert if critical path
```

### 4.2 Circuit Breaker Pattern

```
State: CLOSED (normal)
  ├─ Requests flow normally
  └─ Count failures

Failure threshold: 5 consecutive failures
  │
  ▼

State: OPEN (circuit broken)
  ├─ Reject all requests
  ├─ Redirect to fallback
  └─ Wait 30 seconds

After 30s timeout:
  │
  ▼

State: HALF_OPEN (testing)
  ├─ Allow 1 test request
  ├─ If success → CLOSED
  └─ If failure → OPEN (restart timer)
```

### 4.3 Fallback Strategies

| System | Fallback | Impact |
|--------|----------|--------|
| **xAI down** | Use last known predictions (max 24h old) | Reduced accuracy, acceptable |
| **HHU down** | Queue events in Drift Money (FIFO) | Delayed but no data loss |
| **META down** | GOK:AI runs without social context | Functional but less optimal |
| **Drift Money down** | STOP all transfers, escalate to CTO | Financial safety prioritized |
| **GOK:AI down** | All systems degrade to local operation | Integrated operations cease |

---

## 5. MONITORING & OBSERVABILITY HOOKS

### 5.1 Metrics to Track

```
Per message:
  - latency (p50, p95, p99)
  - success_rate (200/total)
  - error_rate (5xx/total)
  - queue_depth
  - retry_count

Per system integration:
  - availability (%)
  - message_throughput (msgs/sec)
  - integration_health_score (0-1)
  - dependency_status (operational|degraded|down)
```

### 5.2 Health Check Endpoint

```
Every system exposes:
  GET /health/oip
  
  Response:
  {
    "status": "operational|degraded|down",
    "system": "gok-ai",
    "dependencies": {
      "xai": "operational",
      "hhu": "operational",
      "meta": "degraded",
      "drift": "operational"
    },
    "last_message_received": "2026-02-04T10:00:00Z",
    "response_time_ms": 45,
    "integration_health": 0.98
  }
```

### 5.3 Alert Rules

| Condition | Severity | Action |
|-----------|----------|--------|
| System response time >2s | WARNING | Log, monitor |
| System response time >5s | CRITICAL | Page on-call |
| Error rate >5% | WARNING | Log, ticket |
| Error rate >10% | CRITICAL | Page, escalate |
| Circuit breaker OPEN | CRITICAL | Immediate escalation |
| Message loss detected | CRITICAL | Incident response |

---

## 6. IMPLEMENTATION ROADMAP

### Phase 1: Core (Days 1-4)
- [ ] Design JSON schemas (all message types)
- [ ] Define security model (JWT, TLS)
- [ ] Build auth server prototype
- [ ] Create OpenAPI spec

### Phase 2: Framework (Days 5-8)
- [ ] Build OIP router (Express/Go)
- [ ] Implement retry + circuit breaker
- [ ] Add monitoring hooks
- [ ] Create SDK for each system

### Phase 3: Integration (Days 9-12)
- [ ] Integrate GOK:AI ↔ xAI
- [ ] Integrate HHU ↔ Drift Money
- [ ] Integrate META ↔ HHU
- [ ] End-to-end testing

---

## 7. SUCCESS CRITERIA

By Day 12:
- [ ] All 5 systems can send/receive messages via OIP
- [ ] Zero message loss in normal operation
- [ ] Circuit breaker triggers correctly when system down
- [ ] JWT tokens verified in <10ms
- [ ] 99.9% uptime in test environment
- [ ] Health checks return accurate system status

---

**Status: SPECIFICATION READY FOR IMPLEMENTATION**

*Data: 4 lutego 2026*
*Autoryzacja: META-GENIUSZ PATRYK SOBIERAŃSKI*
