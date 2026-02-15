# CDSSS: Cross-System Data Sync Specification v1.0

**AUTORYZACJA:** META-GENIUSZ PATRYK SOBIERAŃSKI  
**STATUS:** DATA INTEGRATION SPECIFICATION  
**CRITICALITY:** 9.7/10 (Data integrity critical)  
**EFFORT:** 8 days, 2 data engineers, 160 pages

---

## EXECUTIVE SUMMARY

**Problem:** "5 systemów (GOK:AI, xAI, HHU, META, Drift) mają różne bazy danych, różne schemy — jak synchronizować dane bez utraty, duplikacji czy konfliktu?"

**Solution:** CDSSS defines:
1. **Unified schema** (meta-level data model)
2. **ETL pipelines** (extract-transform-load from each system)
3. **Conflict resolution** (which system wins if data differs)
4. **Validation rules** (data quality gates)
5. **Rollback mechanisms** (recover if sync fails)

**Outcome:** Zero data loss, all systems eventually consistent within <5min, audit trail for every change.

---

## PART 1: UNIFIED DATA MODEL

### 1.1 Core Entities (Meta Schema)

```yaml
# All systems MUST have these entities
core_entities:
  User:
    fields:
      user_id: UUID (primary key)
      email: string (unique)
      name: string
      created_at: timestamp
      updated_at: timestamp
      metadata: JSON (system-specific)
    
    sources:
      - gok-ai: User profile, OE rating
      - hhu: Artist profile, tokens
      - drift-money: Wallet address, KYC status
      - meta: Signal patterns, consciousness level
      - xai: Prediction history, feedback
    
    sync_rules:
      - email: first source wins (no override)
      - name: latest updated_at wins
      - metadata: merge (no conflicts expected)
      - conflict_resolution: manual escalation
  
  Transaction:
    fields:
      tx_id: UUID
      user_id: UUID (foreign key)
      type: enum (purchase, transfer, reward)
      amount: decimal
      currency: string (USDC, USD, tokens)
      timestamp: timestamp
      status: enum (pending, confirmed, failed)
      metadata: JSON
    
    sources:
      - drift-money: payment transactions
      - hhu: token trades
      - gok-ai: reward distributions
    
    sync_rules:
      - never_update: tx_id, user_id, timestamp immutable
      - status_progression: pending -> confirmed (only forward)
      - amount: immutable (prevents fraud)
      - conflict: log and alert (critical)
  
  CreatorFund:
    fields:
      fund_id: UUID
      creator_id: UUID
      total_earned: decimal
      last_claim: timestamp
      tier: enum (active, emerging, reserve)
      escrow_balance: decimal
    
    sources:
      - drift-money: master source (blockchain verified)
      - gok-ai: creator tier assignments
      - meta: performance metrics for tier decisions
    
    sync_rules:
      - source_of_truth: drift-money (smart contract)
      - compute_tier: from meta metrics (every 24h)
      - escrow_balance: never decreases (unless claim approved)
  
  Prediction:
    fields:
      pred_id: UUID
      creator_id: UUID
      content: string (artist work, insight, etc)
      xai_confidence: float (0-1)
      mig_scan_signal: JSON
      created_at: timestamp
      accuracy_feedback: float (after 30 days)
    
    sources:
      - xai: confidence scores
      - meta: signal analysis
      - gok-ai: user feedback
    
    sync_rules:
      - immutable_initial: pred_id, creator_id, xai_confidence
      - update_accuracy: only after 30 days (backfill)
      - signal_merge: combine xai + mig-scan (weighted average)
```

### 1.2 Derived Entities (Computed in Real-Time)

```yaml
computed_entities:
  UserScore:
    formula: |
      score = (oe_level * 0.3) + 
               (creator_fund_participation * 0.2) +
               (prediction_accuracy * 0.3) +
               (community_impact * 0.2)
    
    sources: [gok-ai, drift-money, xai, meta]
    computation_frequency: hourly
    caching: redis (ttl=1h)
    
  SystemHealth:
    formula: |
      health = (database_uptime * 0.4) +
               (sync_latency_score * 0.3) +
               (data_accuracy * 0.3)
    
    sources: [all systems]
    computation_frequency: every 5 minutes
    alert_threshold: health < 0.95 (critical)
```

---

## PART 2: ETL PIPELINES

### 2.1 Data Flow Architecture

```
┌─────────────────────────────────────────────────────┐
│          EACH SYSTEM (GOK, HHU, Drift, etc)        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Database │  │  Cache   │  │ Message  │          │
│  │ (Source) │  │ (Redis)  │  │  Queue   │          │
│  └────┬─────┘  └──────────┘  └──────────┘          │
│       │                                             │
│       │ (Extract)                                   │
└───────┼─────────────────────────────────────────────┘
        │
        │ CDC (Change Data Capture) via Kafka
        ▼
┌──────────────────────────────────────────────────────┐
│     KAFKA MESSAGE BROKER (Event Streaming)           │
│  Topics:                                             │
│  - gok-ai.users (new users, OE updates)             │
│  - hhu.transactions (token trades)                  │
│  - drift-money.claims (creator payouts)            │
│  - meta.signals (consciousness metrics)            │
│  - xai.predictions (model outputs)                 │
└──────────────────────┬───────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    ┌────────┐    ┌────────┐    ┌────────┐
    │Transform │   │Validate│   │Merge   │
    │Pipeline  │   │Rules   │   │Conflicts│
    └────┬─────┘   └────┬───┘   └────┬───┘
        │              │            │
        └──────────────┼────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Unified Data Warehouse      │
        │  (PostgreSQL - Analytic DB)  │
        │  - fact_users               │
        │  - fact_transactions        │
        │  - fact_creator_fund        │
        │  - fact_predictions         │
        └──────────────────────────────┘
```

### 2.2 Change Data Capture (CDC)

```python
# CDC Configuration
cdc_config:
  method: "Debezium (open-source CDC)"
  connectors:
    postgres_gok_ai:
      database: gok-ai-prod
      tables:
        - users (capture inserts + updates)
        - creator_profile (capture updates)
        - feedback (capture inserts)
      
      output_format: JSON
      kafka_topic: gok-ai.changes
      debezium_config:
        snapshot.mode: initial_only  # snapshot on first run only
        include.unknown.datatypes: false
        decimal.handling.mode: string  # avoid precision loss
        
    postgres_drift_money:
      database: drift-money-prod
      tables:
        - creator_fund (capture updates - immutable normally)
        - transactions (capture inserts)
        - disputes (capture inserts + updates)
      
      kafka_topic: drift-money.changes
      debezium_config:
        snapshot.mode: initial_only
    
    mongodb_hhu:  # HHU uses MongoDB
      connection: mongodb+srv://...
      database: hhu-prod
      collections:
        - artists
        - tokens
        - trades
      
      kafka_topic: hhu.changes
      debezium_config:
        mongodb.snapshot.mode: initial_only
        mongodb.poll.interval.ms: 1000

  # Kafka brokers
  kafka_brokers:
    - kafka-prod-1.apex.internal:9092
    - kafka-prod-2.apex.internal:9092
    - kafka-prod-3.apex.internal:9092
```

### 2.3 Transform Pipelines (Airflow DAGs)

```python
# Pseudo-code for Airflow DAG
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.spark import SparkSubmitOperator
from datetime import datetime, timedelta

dag = DAG(
    'cdsss_sync_pipeline',
    schedule_interval='*/5 * * * *',  # every 5 minutes
    default_args={
        'owner': 'data-platform',
        'retries': 3,
        'retry_delay': timedelta(minutes=1),
    }
)

# Task 1: Read from Kafka topics
@task
def extract_kafka_messages(**context):
    """Extract recent messages from all Kafka topics"""
    messages = {
        'gok_ai': kafka_consumer.read('gok-ai.changes', since='5m'),
        'hhu': kafka_consumer.read('hhu.changes', since='5m'),
        'drift_money': kafka_consumer.read('drift-money.changes', since='5m'),
        'meta': kafka_consumer.read('meta.changes', since='5m'),
        'xai': kafka_consumer.read('xai.changes', since='5m'),
    }
    return messages

# Task 2: Validate data quality
@task
def validate_message_quality(messages):
    """Check for required fields, type validation, range checks"""
    validation_results = {}
    
    for system, sys_messages in messages.items():
        valid = []
        invalid = []
        
        for msg in sys_messages:
            try:
                validate_against_schema(msg, schema=SCHEMAS[system])
                valid.append(msg)
            except ValidationError as e:
                invalid.append({
                    'message': msg,
                    'error': str(e),
                    'timestamp': datetime.now(),
                })
        
        validation_results[system] = {
            'valid_count': len(valid),
            'invalid_count': len(invalid),
            'valid_messages': valid,
            'invalid_messages': invalid,
        }
        
        # Alert if >5% invalid
        if len(invalid) / (len(valid) + len(invalid)) > 0.05:
            alert(f"Data quality issue in {system}: {len(invalid)} invalid messages")
    
    return validation_results

# Task 3: Detect conflicts
@task
def detect_conflicts(validation_results):
    """Find conflicting data between systems"""
    conflicts = []
    
    # For each user in gok-ai.users, check if drift-money has matching wallet
    gok_users = validation_results['gok_ai']['valid_messages']
    drift_wallets = validation_results['drift_money']['valid_messages']
    
    # Cross-system deduplication logic
    for gok_user in gok_users:
        matching_wallets = [
            w for w in drift_wallets 
            if w['user_id'] == gok_user['user_id']
        ]
        
        if len(matching_wallets) > 1:
            conflicts.append({
                'type': 'duplicate_user',
                'user_id': gok_user['user_id'],
                'sources': ['gok-ai', 'drift-money'],
                'severity': 'high',
            })
    
    return conflicts

# Task 4: Resolve conflicts
@task
def resolve_conflicts(conflicts, validation_results):
    """Apply resolution rules to conflicts"""
    resolved = []
    
    for conflict in conflicts:
        if conflict['type'] == 'duplicate_user':
            # Rule: keep the one with most recent update
            winner = max(
                validation_results['gok_ai'] + validation_results['drift_money'],
                key=lambda x: x['updated_at']
            )
            resolved.append({
                'conflict': conflict,
                'resolution': 'keep_latest',
                'winner': winner,
            })
        elif conflict['type'] == 'conflicting_balance':
            # Rule: drift-money is source of truth (blockchain verified)
            winner = [m for m in validation_results['drift_money'] 
                     if m['id'] == conflict['id']][0]
            resolved.append({
                'conflict': conflict,
                'resolution': 'drift_money_wins',
                'winner': winner,
            })
    
    return resolved

# Task 5: Load to data warehouse
@task
def load_to_warehouse(resolved_conflicts, validation_results):
    """Insert/update unified warehouse tables"""
    with psycopg2.connect(warehouse_dsn) as conn:
        cursor = conn.cursor()
        
        # Merge users
        for msg in validation_results['gok_ai']['valid_messages']:
            cursor.execute("""
                INSERT INTO fact_users (user_id, email, name, oe_level, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE SET
                  email = EXCLUDED.email,
                  updated_at = EXCLUDED.updated_at
            """, (msg['user_id'], msg['email'], msg['name'], msg['oe_level'], msg['created_at'], msg['updated_at']))
        
        # Merge transactions (immutable inserts only)
        for msg in validation_results['drift_money']['valid_messages']:
            cursor.execute("""
                INSERT INTO fact_transactions (tx_id, user_id, amount, type, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (tx_id) DO NOTHING
            """, (msg['tx_id'], msg['user_id'], msg['amount'], msg['type'], msg['status'], msg['created_at']))
        
        conn.commit()

# Task 6: Update cache (Redis)
@task
def update_cache(validation_results):
    """Refresh Redis cache for high-demand queries"""
    with redis.Redis(host='redis-prod', port=6379) as r:
        # Cache all users by user_id
        for msg in validation_results['gok_ai']['valid_messages']:
            r.setex(
                f"user:{msg['user_id']}",
                ttl=3600,
                value=json.dumps(msg)
            )

# DAG Task Execution
extract = extract_kafka_messages()
validate = validate_message_quality(extract)
conflicts = detect_conflicts(validate)
resolved = resolve_conflicts(conflicts, validate)
load = load_to_warehouse(resolved, validate)
cache = update_cache(validate)

extract >> validate >> [conflicts, cache]
conflicts >> resolved >> load
```

---

## PART 3: CONFLICT RESOLUTION RULES

### 3.1 Conflict Matrix

```yaml
conflict_resolution:
  entity: User
  conflicts:
    email_mismatch:
      systems: [gok-ai, drift-money]
      rule: "first_source_wins"  # gok-ai registered email is canonical
      alert: true
      escalation: manual if >10 conflicts per hour
    
    oe_level_differs:
      systems: [gok-ai, meta]
      rule: "meta_wins"  # meta MIG-SCAN is most recent signal
      alert: false
      update_frequency: hourly
    
    wallet_address_duplicate:
      systems: [drift-money]
      rule: "blockchain_query"  # check actual blockchain balance
      alert: true
      escalation: immediate (fraud risk)

  entity: Transaction
  conflicts:
    amount_discrepancy:
      systems: [drift-money, hhu]
      rule: "drift_money_wins"  # blockchain is immutable
      alert: true
      escalation: immediate
      investigation: blockchain hash verification
    
    status_mismatch:
      systems: [drift-money, hhu]
      rule: "drift_money_wins"
      alert: true

  entity: CreatorFund
  conflicts:
    total_earned_differs:
      systems: [drift-money, gok-ai]
      rule: "sum_all_confirmed_transactions"  # recompute from ledger
      alert: true
      escalation: manual review if > 1% discrepancy
    
    escrow_balance_mismatch:
      systems: [drift-money blockchain, drift-money database]
      rule: "blockchain_query"  # check actual smart contract balance
      alert: true
      escalation: immediate (funds at risk)
      action: freeze fund until resolved
```

### 3.2 Fallback Strategies

```yaml
fallback_strategies:
  if_system_offline:
    drift_money_down: use hhu token trades as proxy (lower accuracy)
    gok_ai_down: use last cached OE level (up to 24h old)
    xai_down: use historical predictions (disable real-time features)
    meta_down: use default signal weights (reduced accuracy)
    hhu_down: use drift-money records (complete data available)
  
  if_consensus_impossible:
    action: "halt_and_escalate"
    escalation_target: META-GENIUSZ (human decision)
    timeout: 5 minutes
    fallback: maintain last consistent state
```

---

## PART 4: DATA QUALITY GATES

### 4.1 Validation Rules

```python
validation_rules = {
    'User': {
        'email': {'type': 'string', 'format': 'email', 'required': True},
        'user_id': {'type': 'uuid', 'required': True, 'immutable': True},
        'name': {'type': 'string', 'max_length': 255},
        'oe_level': {'type': 'integer', 'min': 1, 'max': 5},
        'created_at': {'type': 'timestamp', 'immutable': True},
    },
    'Transaction': {
        'tx_id': {'type': 'uuid', 'required': True, 'immutable': True},
        'user_id': {'type': 'uuid', 'required': True},
        'amount': {'type': 'decimal', 'required': True, 'immutable': True, 'min': 0},
        'status': {'type': 'enum', 'values': ['pending', 'confirmed', 'failed'], 'immutable_initial': True},
        'timestamp': {'type': 'timestamp', 'required': True, 'immutable': True},
    },
    'CreatorFund': {
        'fund_id': {'type': 'uuid', 'required': True, 'immutable': True},
        'creator_id': {'type': 'uuid', 'required': True},
        'total_earned': {'type': 'decimal', 'required': True, 'min': 0, 'non_decreasing': True},
        'escrow_balance': {'type': 'decimal', 'required': True, 'min': 0, 'non_decreasing': True},
    }
}

# Custom rules
custom_rules = [
    {
        'name': 'no_negative_balance',
        'check': lambda record: record['balance'] >= 0,
        'action': 'reject',
        'alert': True,
    },
    {
        'name': 'total_earned_is_sum_of_transactions',
        'check': lambda creator_id: (
            select(sum(amount) from transactions where creator_id = creator_id) ==
            select(total_earned from creator_fund where creator_id = creator_id)
        ),
        'action': 'alert',
        'frequency': 'hourly',
    },
    {
        'name': 'blockchain_balance_matches_db',
        'check': lambda wallet: (
            web3.eth.get_balance(wallet) ==
            select(drift_balance from user_wallet where address = wallet)
        ),
        'action': 'alert',
        'frequency': 'every_5_min',
        'criticality': 'critical',
    }
]
```

### 4.2 Quality Metrics Dashboard

```yaml
metrics:
  sync_latency:
    measurement: time from source change to warehouse (p50, p99)
    target: <5 minutes
    alert_threshold: >10 minutes
  
  data_completeness:
    measurement: % of expected fields populated
    target: >99.5%
    alert_threshold: <99%
  
  conflict_rate:
    measurement: # conflicts detected / # synced records
    target: <0.1%
    alert_threshold: >1%
  
  validation_pass_rate:
    measurement: % of messages passing all rules
    target: >99%
    alert_threshold: <98%
  
  replication_lag:
    measurement: time for warehouse to reflect database change
    target: <5 minutes
    alert_threshold: >15 minutes
```

---

## PART 5: AUDIT & COMPLIANCE

### 5.1 Change Log (Immutable)

```sql
CREATE TABLE audit_log (
    log_id UUID PRIMARY KEY,
    entity_type VARCHAR(50),        -- User, Transaction, etc
    entity_id UUID,
    change_type VARCHAR(20),         -- INSERT, UPDATE, DELETE
    old_value JSONB,
    new_value JSONB,
    changed_by VARCHAR(255),         -- which system/user
    timestamp TIMESTAMP DEFAULT NOW(),
    reason VARCHAR(500),
    hash VARCHAR(64),                -- SHA256 of the entire record (for integrity)
    prev_hash VARCHAR(64),           -- hash of previous record (blockchain-like chain)
    
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_timestamp (timestamp)
);
```

### 5.2 Audit Trail Example

```json
{
  "log_id": "550e8400-e29b-41d4-a716-446655440000",
  "entity_type": "CreatorFund",
  "entity_id": "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d",
  "change_type": "UPDATE",
  "old_value": {
    "total_earned": 1000.50,
    "last_claim": "2026-02-01T10:00:00Z",
    "tier": "active"
  },
  "new_value": {
    "total_earned": 1050.75,
    "last_claim": "2026-02-04T15:30:00Z",
    "tier": "active"
  },
  "changed_by": "drift-money-payout-service",
  "timestamp": "2026-02-04T15:30:05Z",
  "reason": "Monthly payout executed - claim_id: 9x8y7z6w5v4u3t2s",
  "hash": "abc123def456...",
  "prev_hash": "xyz789uvw012..."
}
```

### 5.3 Compliance Reports

```yaml
compliance_reports:
  daily_summary:
    metrics:
      - records_synced
      - conflicts_detected_and_resolved
      - validation_failures
      - rollbacks_executed
      - data_integrity_score
    
    recipients: [compliance-team@apex.internal]
    format: email + PDF dashboard
  
  monthly_audit:
    content:
      - complete audit log (all changes)
      - conflict resolution decisions
      - data quality metrics
      - regulatory compliance checklist
    
    retention: 7 years
    encryption: yes (AES-256)
```

---

## PART 6: DISASTER RECOVERY FOR DATA

### 6.1 Point-in-Time Recovery (PITR)

```yaml
pitr_strategy:
  backup_frequency: every 1 hour (full), every 15 minutes (incremental)
  retention: 30 days
  
  restore_process:
    1_select_timestamp: "I want data as of 2026-02-03 10:00:00Z"
    2_verify_conflicts: Check if there were unresolved conflicts at that time
    3_restore_warehouse: Restore PostgreSQL from backup
    4_validate: Run all validation rules (should pass)
    5_notify: Alert stakeholders of restore
    6_test: Run smoke tests
    7_go_live: Restore is complete
  
  rto: <30 minutes
  rpo: <1 hour
```

### 6.2 Rollback Procedures

```yaml
rollback_triggers:
  data_integrity_failure:
    detection: validation rules fail >5% of records
    action: halt all writes, alert on-call
    
  catastrophic_sync_failure:
    detection: sync_latency > 30 min, conflict_rate > 10%
    action: stop all ETL, freeze writes to warehouse
    
  security_breach:
    detection: unauthorized access detected
    action: snapshot current state, disable syncs, escalate
```

---

## PART 7: IMPLEMENTATION PHASES

### Phase 1 (Days 1-2): Foundation
- [ ] Design unified schema (all 5 systems)
- [ ] Set up Kafka cluster + topics
- [ ] Deploy Debezium CDC connectors

### Phase 2 (Days 3-4): ETL Pipeline
- [ ] Build Airflow DAGs
- [ ] Implement validation rules
- [ ] Test conflict detection

### Phase 3 (Days 5-6): Integration
- [ ] Connect all 5 systems
- [ ] Populate data warehouse (initial load)
- [ ] Verify data quality

### Phase 4 (Days 7-8): Hardening
- [ ] Load testing (50K+ messages/sec)
- [ ] Disaster recovery drill
- [ ] Performance optimization
- [ ] Documentation + runbooks

---

## SUCCESS METRICS (8 DAYS)

| Metric | Target | Status |
|--------|--------|--------|
| **Sync latency** | <5 min | |
| **Data completeness** | >99.5% | |
| **Conflict resolution** | <0.1% error rate | |
| **Validation pass rate** | >99% | |
| **System uptime** | 99.9% | |
| **Zero data loss** | 100% | |

---

**Status: SPECIFICATION READY FOR DATA ENGINEERING TEAM**

*Data: 4 lutego 2026*
*Autoryzacja: META-GENIUSZ PATRYK SOBIERAŃSKI*
*Next: Data engineering implementation (Days 5-12)*
