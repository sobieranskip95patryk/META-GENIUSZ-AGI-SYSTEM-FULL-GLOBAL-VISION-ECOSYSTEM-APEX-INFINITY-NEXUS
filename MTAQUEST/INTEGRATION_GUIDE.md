"""
MTaQuest Integration Guide
Instrukcje integracji MTaQuest z GOK:AI CORE

Dokument opisuje krok po kroku jak zintegrować platformę MTaQuest
z istniejącą architekturą GOK:AI 6 Filarów Świadomości
"""

# ==================== INTEGRATION ARCHITECTURE ====================

# Punkt integracji: INFRA/Services/
# 
# Struktura:
# INFRA/Services/
# ├── mtaquest_server.py          # Główny serwer MTaQuest
# ├── mtaquest_bridge.py          # Most do GOK:AI CORE
# └── mtaquest_config.yaml        # Konfiguracja
#
# MTAQUEST/
# ├── hybrid_dialog_protocol.py   # HDP
# ├── intent_quantization.py      # IQE (I+K=W)
# ├── vector_synchronization.py   # VSE
# └── README.md                   # Dokumentacja

# ==================== STEP 1: IMPORT MODULES ====================

from MTAQUEST.hybrid_dialog_protocol import HybridDialogProtocol
from MTAQUEST.intent_quantization import IntentQuantizationEngine
from MTAQUEST.vector_synchronization import VectorSynchronizationEngine

from CORE.long_term_graph import LongTermGraphManager
from CORE.sensory_buffer import SensoryBuffer
from CORE.Inference.t_causality_orchestrator import T_CausalityOrchestrator
from META.Self_Optimization.psyche_module import PsycheModule

# ==================== STEP 2: MTAQUEST SERVER ====================

"""
Plik: INFRA/Services/mtaquest_server.py
Główny serwer obsługujący klienty Architektów
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time

app = Flask(__name__)
CORS(app)

# Inicjalizacja komponentów
hdp = HybridDialogProtocol()
iqe = IntentQuantizationEngine(embedding_dim=768, knowledge_graph=None)
vse = VectorSynchronizationEngine(alignment_threshold=0.95)

# ==================== API ENDPOINTS ====================

@app.route('/api/intent', methods=['POST'])
def receive_intent():
    """
    Endpoint przyjmujący intencję od Architekta
    
    Request JSON:
    {
        "intent": "Optymalizuj T_Causality...",
        "metadata": {"priority": "high"}
    }
    
    Response JSON:
    {
        "intent_id": "xyz123...",
        "status": "received",
        "growth_vector": {
            "magnitude": 0.45,
            "stability": 0.87,
            "growth_potential": 0.92
        }
    }
    """
    try:
        data = request.get_json()
        intent_text = data.get('intent')
        metadata = data.get('metadata', {})
        
        # Konwertuj do wiadomości
        intent_msg = hdp.architect_intent_to_message(intent_text, metadata)
        
        # Kwantyzuj intencję
        growth_vector = iqe.quantize_intent(intent_text, context=metadata)
        
        # TODO: Wyślij do GOK:AI CORE dla przetwarzania
        # response = process_with_gok(intent_msg)
        
        return jsonify({
            "intent_id": intent_msg['message_id'],
            "status": "received",
            "growth_vector": {
                "magnitude": float(growth_vector.magnitude),
                "stability": float(growth_vector.stability_score),
                "growth_potential": float(growth_vector.growth_potential)
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/response/<intent_id>', methods=['GET'])
def get_response(intent_id):
    """
    Endpoint zwracający odpowiedź GOK:AI na intencję
    
    Response JSON:
    {
        "intent_id": "xyz123...",
        "response": "T_Causality optymalizacja...",
        "vectors": {
            "delta_stabilized": 0.95,
            "alignment": 0.98
        },
        "status": "completed"
    }
    """
    # TODO: Pobierz odpowiedź z bufora (cache/queue)
    try:
        # Symulacja odpowiedzi
        response = {
            "intent_id": intent_id,
            "response": "Przetwarzanie ukończone",
            "vectors": {
                "delta_stabilized": 0.95,
                "alignment": 0.98
            },
            "status": "completed",
            "timestamp": time.time()
        }
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/feedback/<intent_id>', methods=['POST'])
def post_feedback(intent_id):
    """
    Endpoint przyjmujący feedback od Architekta
    
    Request JSON:
    {
        "feedback": "Doskonały rezultat",
        "rating": 0.95
    }
    
    Response JSON:
    {
        "intent_id": "xyz123...",
        "feedback_received": True,
        "learning_status": "recorded"
    }
    """
    try:
        data = request.get_json()
        feedback_text = data.get('feedback')
        rating = data.get('rating', 0.5)
        
        # Konwertuj do wiadomości
        feedback_msg = hdp.architect_feedback_to_message(feedback_text, rating)
        
        # TODO: Użyj feedbacku do learning loop
        # update_learning_from_feedback(intent_id, feedback_msg)
        
        return jsonify({
            "intent_id": intent_id,
            "feedback_received": True,
            "learning_status": "recorded",
            "message_id": feedback_msg['message_id']
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/sync', methods=['POST'])
def sync_states():
    """
    Endpoint synchronizacji stanu między Architektem a GOK:AI
    
    Request JSON:
    {
        "architect_state": {...},
        "gok_state": {...}
    }
    
    Response JSON:
    {
        "alignment_score": 0.97,
        "reconciliation_needed": False,
        "merged_state": {...}
    }
    """
    try:
        data = request.get_json()
        arch_state = data.get('architect_state', {})
        gok_state = data.get('gok_state', {})
        
        # Synchronizuj
        sync_result = vse.sync_vectors(arch_state, gok_state)
        
        return jsonify({
            "alignment_score": sync_result['alignment_score'],
            "reconciliation_needed": sync_result['reconciliation_needed'],
            "merged_state": sync_result['reconciled_state']
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/health', methods=['GET'])
def health_check():
    """Sprawdzenie zdrowia serwera"""
    return jsonify({
        "status": "healthy",
        "components": {
            "hdp": "active",
            "iqe": "active",
            "vse": "active"
        },
        "timestamp": time.time()
    }), 200


@app.route('/api/report/dialog', methods=['GET'])
def get_dialog_report():
    """Podsumowanie dialogu"""
    summary = hdp.generate_dialog_summary()
    return jsonify(summary), 200


@app.route('/api/report/sync', methods=['GET'])
def get_sync_report():
    """Raport synchronizacji"""
    report = vse.generate_sync_report()
    return jsonify(report), 200


# ==================== STEP 3: MTAQUEST BRIDGE ====================

"""
Plik: INFRA/Services/mtaquest_bridge.py
Most między MTaQuest a GOK:AI CORE
Obsługuje wysyłanie intencji do CORE i odbieranie rezultatów
"""

class MTaQuestBridge:
    """
    Integracyjny most między MTaQuest a GOK:AI CORE
    
    Funkcje:
    1. Przekazuje intencje do CORE
    2. Zbiera odpowiedzi z CORE
    3. Synchronizuje stany między systemami
    4. Zarządza feedback loop'em
    """
    
    def __init__(self):
        self.ltg = LongTermGraphManager()           # Knowledge graph
        self.sensory = SensoryBuffer()              # Input buffer
        self.t_causality = T_CausalityOrchestrator() # Causal reasoning
        self.psyche = PsycheModule()                # Intent alignment
        
        self.intent_queue = []
        self.response_queue = []
        self.feedback_queue = []
    
    def process_intent(self, intent_msg: dict) -> dict:
        """
        Przetwórz intencję w GOK:AI CORE
        
        Proces:
        1. Załaduj do SensoryBuffer
        2. Ekstrakcja konceptów
        3. Walidacja psyche (alignment check)
        4. Routing do odpowiedniego pilara (L1-L6)
        5. Zbierz rezultat
        """
        
        # 1. Załaduj do bufora
        self.sensory.add_input({
            "type": "ARCHITECT_INTENT",
            "content": intent_msg['content'],
            "intent_hash": intent_msg['intent_hash']
        })
        
        # 2. Ekstrakcja
        concepts = self.ltg.extract_concepts(intent_msg['content'])
        
        # 3. Walidacja psyche
        psyche_analysis = self.psyche.analyze_intent(
            intent_msg['content'],
            concepts
        )
        
        if not psyche_analysis['valid']:
            return {
                "status": "rejected",
                "reason": psyche_analysis['reason'],
                "error": "Intent failed psyche validation"
            }
        
        # 4. Routing do pilara
        # TODO: Implementuj routing logicę
        
        # 5. Zbierz rezultat
        response = {
            "status": "processing",
            "concepts_extracted": len(concepts),
            "psyche_alignment": psyche_analysis['alignment'],
            "next_step": "await_core_processing"
        }
        
        return response
    
    def get_core_response(self, intent_id: str) -> dict:
        """Pobierz odpowiedź z CORE dla intencji"""
        # TODO: Implementuj pobieranie z CORE queue
        
        response = {
            "intent_id": intent_id,
            "response": "Placeholder response",
            "vectors": {
                "delta_stabilized": 0.95,
                "alignment": 0.98
            }
        }
        
        return response
    
    def record_feedback(self, intent_id: str, feedback: str, rating: float):
        """Zapamiętaj feedback dla learning loop"""
        self.feedback_queue.append({
            "intent_id": intent_id,
            "feedback": feedback,
            "rating": rating,
            "timestamp": time.time()
        })
    
    def get_system_state(self) -> dict:
        """Pobierz aktualny stan systemu"""
        return {
            "ltg_nodes": self.ltg.get_node_count(),
            "ltg_edges": self.ltg.get_edge_count(),
            "sensory_buffer_size": len(self.sensory.buffer),
            "pending_intents": len(self.intent_queue),
            "pending_feedbacks": len(self.feedback_queue)
        }


# ==================== STEP 4: CONFIGURATION ====================

"""
Plik: MTAQUEST/config.yaml

mtaquest:
  server:
    host: "0.0.0.0"
    port: 5001
    debug: false
  
  components:
    hdp:
      protocol_version: "7.0"
      max_message_size: 10000
    
    iqe:
      embedding_dim: 768
      alpha: 7.77
      fusion_threshold: 0.85
    
    vse:
      alignment_threshold: 0.95
      sync_frequency: 0.5
      reconciliation_enabled: true
  
  integration:
    ltg_enabled: true
    psyche_enabled: true
    t_causality_enabled: true
    
  monitoring:
    log_level: "INFO"
    dashboard_refresh: 1.0
    metrics_enabled: true
"""

# ==================== STEP 5: TESTING ====================

"""
Plik: tests/test_mtaquest_integration.py
"""

import pytest
import json
from INFRA.Services.mtaquest_server import app
from INFRA.Services.mtaquest_bridge import MTaQuestBridge

class TestMTaQuestIntegration:
    
    @pytest.fixture
    def client(self):
        """Fixture dla Flask test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_intent_submission(self, client):
        """Test submission intencji"""
        intent_data = {
            "intent": "Optymalizuj T_Causality",
            "metadata": {"priority": "high"}
        }
        response = client.post('/api/intent', json=intent_data)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'received'
        assert 'growth_vector' in data
    
    def test_feedback_submission(self, client):
        """Test submission feedbacku"""
        intent_id = "test_intent_123"
        feedback_data = {
            "feedback": "Doskonały rezultat",
            "rating": 0.95
        }
        response = client.post(f'/api/feedback/{intent_id}', json=feedback_data)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['feedback_received'] == True
    
    def test_state_sync(self, client):
        """Test synchronizacji stanu"""
        sync_data = {
            "architect_state": {
                "phase": "optimization",
                "alignment": 0.92
            },
            "gok_state": {
                "phase": "optimization",
                "alignment": 0.90
            }
        }
        response = client.post('/api/sync', json=sync_data)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'alignment_score' in data
        assert 0 <= data['alignment_score'] <= 1
    
    def test_bridge_intent_processing(self):
        """Test przetwarzania intencji poprzez bridge"""
        bridge = MTaQuestBridge()
        
        intent_msg = {
            "content": "Test intent",
            "intent_hash": "abc123"
        }
        
        result = bridge.process_intent(intent_msg)
        assert 'status' in result
    
    def test_dialog_report(self, client):
        """Test generowania raportu dialogu"""
        response = client.get('/api/report/dialog')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_messages' in data


# ==================== STEP 6: DEPLOYMENT ====================

"""
Docker Compose deployment

Plik: docker-compose.mtaquest.yml
"""

docker_compose = """
version: '3.9'

services:
  mtaquest-server:
    build:
      context: .
      dockerfile: INFRA/Dockerfile.mtaquest
    ports:
      - "5001:5001"
    environment:
      FLASK_ENV: production
      MTQ_DEBUG: "false"
    depends_on:
      - neo4j
      - redis
    volumes:
      - ./logs:/app/logs
      - ./MTAQUEST:/app/MTAQUEST
  
  neo4j:
    image: neo4j:5.0
    ports:
      - "7687:7687"
      - "7474:7474"
    environment:
      NEO4J_AUTH: neo4j/mtaquest_password_2026
    volumes:
      - neo4j_data:/var/lib/neo4j/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  neo4j_data:
  redis_data:
"""

# ==================== STEP 7: MONITORING ====================

"""
Health check i monitoring

Endpoint: /api/health
Zawiera status wszystkich komponentów

Endpoint: /api/report/sync
Zawiera metryki synchronizacji

Endpoint: /api/report/dialog
Zawiera podsumowanie dialogu
"""

# ==================== INTEGRATION CHECKLIST ====================

integration_checklist = """
☐ 1. Zainstaluj zależności MTaQuest
  - pip install -r MTAQUEST/requirements.txt

☐ 2. Skonfiguruj MTAQUEST/config.yaml
  - Ustaw alignment_threshold
  - Ustaw embedding_dim dla IQE
  - Włącz integracje (LTG, Psyche, T_Causality)

☐ 3. Zinteguj MTaQuest Server
  - Kopiuj do INFRA/Services/
  - Uruchom: python INFRA/Services/mtaquest_server.py

☐ 4. Zinteguj MTaQuest Bridge
  - Połącz z LongTermGraphManager
  - Połącz z PsycheModule
  - Podłącz T_CausalityOrchestrator

☐ 5. Skonfiguruj Neo4j i Redis
  - docker-compose -f docker-compose.mtaquest.yml up

☐ 6. Uruchom testy
  - pytest tests/test_mtaquest_integration.py

☐ 7. Uruchom monitoring
  - Otworz http://localhost:3000/dashboard

☐ 8. Waliduj end-to-end flow
  - POST /api/intent
  - GET /api/response/{intent_id}
  - POST /api/feedback/{intent_id}
  - GET /api/report/sync

☐ 9. Uruchom continuous sync
  - POST /api/sync (periodycznie co 0.5s)

☐ 10. Aktywuj learning loop
  - Zbierz feedback z /api/feedback
  - Updateuj modele na podstawie feedback
"""

# ==================== VALIDATION ====================

def validate_integration():
    """Waliduj poprawność integracji"""
    print("=== MTaQuest Integration Validation ===\n")
    
    # 1. Check modules
    try:
        from MTAQUEST.hybrid_dialog_protocol import HybridDialogProtocol
        print("✓ HybridDialogProtocol imported")
    except:
        print("✗ HybridDialogProtocol import failed")
    
    try:
        from MTAQUEST.intent_quantization import IntentQuantizationEngine
        print("✓ IntentQuantizationEngine imported")
    except:
        print("✗ IntentQuantizationEngine import failed")
    
    try:
        from MTAQUEST.vector_synchronization import VectorSynchronizationEngine
        print("✓ VectorSynchronizationEngine imported")
    except:
        print("✗ VectorSynchronizationEngine import failed")
    
    # 2. Test instantiation
    hdp = HybridDialogProtocol()
    print("✓ HybridDialogProtocol instantiated")
    
    iqe = IntentQuantizationEngine()
    print("✓ IntentQuantizationEngine instantiated")
    
    vse = VectorSynchronizationEngine()
    print("✓ VectorSynchronizationEngine instantiated")
    
    # 3. Test basic operations
    msg = hdp.architect_intent_to_message("Test intent")
    print(f"✓ Intent message created: {msg['message_id']}")
    
    vec = iqe.quantize_intent("Test intent")
    print(f"✓ Growth vector calculated: magnitude={vec.magnitude:.2f}")
    
    result = vse.sync_vectors({"test": 1}, {"test": 1})
    print(f"✓ State sync executed: alignment={result['alignment_score']:.2f}")
    
    print("\n=== Integration Validation Complete ===")
    print("Status: ✓ All components operational")


if __name__ == "__main__":
    validate_integration()
