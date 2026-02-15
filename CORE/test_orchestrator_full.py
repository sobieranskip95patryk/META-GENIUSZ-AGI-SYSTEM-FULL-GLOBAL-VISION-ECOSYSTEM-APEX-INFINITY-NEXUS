"""
ORCHESTRATOR v2.0 — FULL TEST SUITE
====================================

Test pełnego pipeline'u z rzeczywistymi embeddings.
Walidacja wszystkich 5 faz orkiestracji.

Test Date: 2026-02-03
"""

import sys
import os

# Dodaj CORE do path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from CORE.orchestrator_v2 import OrchestratorV2, IntentVector
from CORE.integration_layer import UnifiedOrchestrator, ProjectVectorAdapter
import json
import time


def generate_test_embedding(dim: int = 128, seed: int = 42) -> list:
    """Generuj testowy embedding (deterministyczny)."""
    import random
    random.seed(seed)
    return [random.uniform(-1.0, 1.0) for _ in range(dim)]


def test_1_basic_orchestrator():
    """Test 1: Podstawowy orchestrator bez embeddings."""
    print("\n" + "="*70)
    print("TEST 1: Podstawowy orchestrator (bez embeddings)")
    print("="*70)
    
    orchestrator = OrchestratorV2(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True,
        inference_enabled=True,
        log_level="WARNING"
    )
    
    intent = IntentVector(
        intent_id="TEST-001",
        intent_text="Test podstawowy",
        intent_embedding=[],  # Pusty
        priority=0.5
    )
    
    response = orchestrator.process_intent(intent)
    
    assert response.status == "SUCCESS", "Status powinien być SUCCESS"
    assert response.intent_id == "TEST-001", "Intent ID niepoprawny"
    
    print("✓ Test 1 PASSED")
    return True


def test_2_orchestrator_with_embeddings():
    """Test 2: Orchestrator z embeddings (ASQK-7G)."""
    print("\n" + "="*70)
    print("TEST 2: Orchestrator z embeddings (ASQK-7G)")
    print("="*70)
    
    orchestrator = OrchestratorV2(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True,
        log_level="WARNING"
    )
    
    # Generuj embedding 128D
    embedding = generate_test_embedding(dim=128, seed=1)
    
    intent = IntentVector(
        intent_id="TEST-002",
        intent_text="Test z embeddings",
        intent_embedding=embedding,
        priority=0.8
    )
    
    response = orchestrator.process_intent(intent, adaptive_mode=True)
    
    # Walidacje
    assert response.status == "SUCCESS", "Status powinien być SUCCESS"
    assert response.synthesis_result is not None, "Synthesis result powinien istnieć"
    assert response.synthesis_result.status == "Gotowe", "Synteza powinna być Gotowa"
    assert response.synthesis_result.score > 0, "Score powinien być > 0"
    
    print(f"  Synthesis Score: {response.synthesis_result.score:.4f}")
    print(f"  GVS: {response.global_vision_score:.4f}")
    print(f"  Execution Time: {response.execution_time_ms:.2f} ms")
    print("✓ Test 2 PASSED")
    return True


def test_3_meta_synthesis():
    """Test 3: Meta-synteza z wieloma wektorami kontekstowymi."""
    print("\n" + "="*70)
    print("TEST 3: Meta-synteza (ASQK-META)")
    print("="*70)
    
    orchestrator = OrchestratorV2(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True,
        log_level="WARNING"
    )
    
    # Generuj embeddings
    intent_embedding = generate_test_embedding(dim=128, seed=10)
    context_vectors = [
        generate_test_embedding(dim=128, seed=20),
        generate_test_embedding(dim=128, seed=30),
        generate_test_embedding(dim=128, seed=40),
        generate_test_embedding(dim=128, seed=50)
    ]
    
    intent = IntentVector(
        intent_id="TEST-003",
        intent_text="Test meta-syntezy",
        intent_embedding=intent_embedding,
        priority=0.9
    )
    
    response = orchestrator.process_intent(
        intent=intent,
        context_vectors=context_vectors,
        adaptive_mode=True
    )
    
    # Walidacje
    assert response.status == "SUCCESS", "Status powinien być SUCCESS"
    assert response.synthesis_result is not None, "Synthesis result powinien istnieć"
    assert response.meta_synthesis_result is not None, "Meta-synthesis result powinien istnieć"
    assert response.meta_synthesis_result.status == "Gotowe", "Meta-synteza powinna być Gotowa"
    assert len(response.meta_synthesis_result.meta_vector) == 128, "Meta-vector powinien mieć 128 wymiarów"
    
    print(f"  Synthesis Score: {response.synthesis_result.score:.4f}")
    print(f"  Meta Score: {response.meta_synthesis_result.meta_score:.4f}")
    print(f"  Meta Vector Dim: {len(response.meta_synthesis_result.meta_vector)}")
    print(f"  GVS: {response.global_vision_score:.4f}")
    print(f"  Action Vector Dim: {len(response.action_vector)}")
    print(f"  Recommendations: {len(response.recommendations)}")
    print(f"  Execution Time: {response.execution_time_ms:.2f} ms")
    print("✓ Test 3 PASSED")
    return True


def test_4_projectvector_integration():
    """Test 4: Integracja z ProjectVector (UnifiedOrchestrator)."""
    print("\n" + "="*70)
    print("TEST 4: Integracja ProjectVector (UnifiedOrchestrator)")
    print("="*70)
    
    orchestrator = UnifiedOrchestrator(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True,
        globalvision_enabled=True,
        inference_enabled=True
    )
    
    # ProjectVector z embeddings
    project_vector = {
        "ProjectVector": {
            "id": "PV-TEST-004",
            "name": "Test Project — AI Education Platform",
            "domain": "Education/AI",
            "priority": 0.95,
            "intent_embedding": generate_test_embedding(dim=128, seed=100),
            "context": {
                "region": "Global",
                "impact": "High",
                "stage": "MVP"
            }
        }
    }
    
    # Context vectors
    context_vectors = [
        generate_test_embedding(dim=128, seed=101),
        generate_test_embedding(dim=128, seed=102),
        generate_test_embedding(dim=128, seed=103)
    ]
    
    result = orchestrator.process_projectvector(
        project_vector=project_vector,
        context_vectors=context_vectors,
        adaptive_mode=True
    )
    
    # Walidacje
    assert result["status"] == "SUCCESS", "Status powinien być SUCCESS"
    assert result["synthesis_result"] is not None, "Synthesis result powinien istnieć"
    assert result["meta_synthesis_result"] is not None, "Meta-synthesis result powinien istnieć"
    assert result["global_vision_score"] > 0, "GVS powinien być > 0"
    
    print(f"  Intent ID: {result['intent_id']}")
    print(f"  Synthesis Score: {result['synthesis_result']['score']:.4f}")
    print(f"  Meta Score: {result['meta_synthesis_result']['meta_score']:.4f}")
    print(f"  GVS: {result['global_vision_score']:.4f}")
    print(f"  Recommendations: {result['recommendations']}")
    print(f"  Execution Time: {result['execution_time_ms']:.2f} ms")
    print("✓ Test 4 PASSED")
    return True


def test_5_batch_processing():
    """Test 5: Przetwarzanie wsadowe wielu ProjectVectors."""
    print("\n" + "="*70)
    print("TEST 5: Przetwarzanie wsadowe (Batch)")
    print("="*70)
    
    orchestrator = UnifiedOrchestrator(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True
    )
    
    # Wygeneruj 5 ProjectVectors
    project_vectors = []
    for i in range(5):
        pv = {
            "ProjectVector": {
                "id": f"PV-BATCH-{i:03d}",
                "name": f"Batch Project {i}",
                "priority": 0.5 + (i * 0.1),
                "intent_embedding": generate_test_embedding(dim=128, seed=200+i)
            }
        }
        project_vectors.append(pv)
    
    start_time = time.time()
    results = orchestrator.batch_process(
        project_vectors=project_vectors,
        adaptive_mode=True
    )
    total_time = (time.time() - start_time) * 1000
    
    # Walidacje
    assert len(results) == 5, "Powinno być 5 wyników"
    for i, result in enumerate(results):
        assert result["status"] == "SUCCESS", f"Wynik {i} powinien być SUCCESS"
        assert result["synthesis_result"] is not None, f"Synthesis result {i} powinien istnieć"
    
    print(f"  Processed: {len(results)} ProjectVectors")
    print(f"  Total Time: {total_time:.2f} ms")
    print(f"  Avg Time per PV: {total_time/len(results):.2f} ms")
    print("✓ Test 5 PASSED")
    return True


def test_6_high_dimensional_embeddings():
    """Test 6: Embeddings wysokowymiarowe (512D, 768D)."""
    print("\n" + "="*70)
    print("TEST 6: Embeddings wysokowymiarowe (512D, 768D)")
    print("="*70)
    
    orchestrator = OrchestratorV2(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True,
        log_level="WARNING"
    )
    
    # Test 512D
    print("\n  [6.1] Test 512D embeddings...")
    embedding_512 = generate_test_embedding(dim=512, seed=300)
    context_512 = [
        generate_test_embedding(dim=512, seed=301),
        generate_test_embedding(dim=512, seed=302)
    ]
    
    intent_512 = IntentVector(
        intent_id="TEST-006-512D",
        intent_text="Test 512D",
        intent_embedding=embedding_512,
        priority=0.8
    )
    
    response_512 = orchestrator.process_intent(
        intent=intent_512,
        context_vectors=context_512,
        adaptive_mode=True
    )
    
    assert response_512.status == "SUCCESS"
    assert len(response_512.action_vector) == 512
    print(f"    ✓ 512D: Meta-vector dim = {len(response_512.action_vector)}")
    
    # Test 768D
    print("\n  [6.2] Test 768D embeddings...")
    embedding_768 = generate_test_embedding(dim=768, seed=400)
    context_768 = [
        generate_test_embedding(dim=768, seed=401),
        generate_test_embedding(dim=768, seed=402)
    ]
    
    intent_768 = IntentVector(
        intent_id="TEST-006-768D",
        intent_text="Test 768D",
        intent_embedding=embedding_768,
        priority=0.9
    )
    
    response_768 = orchestrator.process_intent(
        intent=intent_768,
        context_vectors=context_768,
        adaptive_mode=True
    )
    
    assert response_768.status == "SUCCESS"
    assert len(response_768.action_vector) == 768
    print(f"    ✓ 768D: Meta-vector dim = {len(response_768.action_vector)}")
    
    print("\n✓ Test 6 PASSED")
    return True


def test_7_adaptive_mode():
    """Test 7: Porównanie trybu standard vs adaptive."""
    print("\n" + "="*70)
    print("TEST 7: Tryb standard vs adaptive")
    print("="*70)
    
    orchestrator = OrchestratorV2(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True,
        log_level="WARNING"
    )
    
    embedding = generate_test_embedding(dim=128, seed=500)
    
    intent = IntentVector(
        intent_id="TEST-007",
        intent_text="Test adaptive mode",
        intent_embedding=embedding,
        priority=0.8
    )
    
    # Standard mode
    response_standard = orchestrator.process_intent(intent, adaptive_mode=False)
    score_standard = response_standard.synthesis_result.score
    
    # Adaptive mode
    response_adaptive = orchestrator.process_intent(intent, adaptive_mode=True)
    score_adaptive = response_adaptive.synthesis_result.score
    
    print(f"  Standard Score: {score_standard:.4f}")
    print(f"  Adaptive Score: {score_adaptive:.4f}")
    print(f"  Różnica: {abs(score_adaptive - score_standard):.4f}")
    
    # W trybie adaptive score powinien się różnić (bo energy modyfikuje faktor)
    assert score_standard != score_adaptive, "Scores powinny się różnić w trybie adaptive"
    
    print("✓ Test 7 PASSED")
    return True


def test_8_error_handling():
    """Test 8: Obsługa błędów i edge cases."""
    print("\n" + "="*70)
    print("TEST 8: Obsługa błędów i edge cases")
    print("="*70)
    
    orchestrator = OrchestratorV2(
        asqk_7g_enabled=True,
        asqk_meta_enabled=True,
        log_level="WARNING"
    )
    
    # Edge case 1: Puste embeddings
    print("\n  [8.1] Puste embeddings...")
    intent_empty = IntentVector(
        intent_id="TEST-008-EMPTY",
        intent_text="Test empty",
        intent_embedding=[],
        priority=0.5
    )
    response_empty = orchestrator.process_intent(intent_empty)
    assert response_empty.status == "SUCCESS"
    print("    ✓ Puste embeddings obsłużone poprawnie")
    
    # Edge case 2: Niezgodne wymiary context vectors
    print("\n  [8.2] Niezgodne wymiary context vectors...")
    intent_128 = IntentVector(
        intent_id="TEST-008-MISMATCH",
        intent_text="Test mismatch",
        intent_embedding=generate_test_embedding(dim=128, seed=600),
        priority=0.5
    )
    context_mismatched = [
        generate_test_embedding(dim=128, seed=601),
        generate_test_embedding(dim=64, seed=602),  # Inny wymiar!
    ]
    
    response_mismatch = orchestrator.process_intent(
        intent_128,
        context_vectors=context_mismatched
    )
    
    # System powinien obsłużyć błąd gracefully
    assert response_mismatch.status == "SUCCESS"
    if response_mismatch.meta_synthesis_result:
        # Jeśli meta-synteza się nie udała, status powinien to pokazać
        assert "Błąd" in response_mismatch.meta_synthesis_result.status or \
               response_mismatch.meta_synthesis_result.status == "Gotowe"
    print("    ✓ Niezgodne wymiary obsłużone poprawnie")
    
    print("\n✓ Test 8 PASSED")
    return True


def run_full_test_suite():
    """Uruchom pełny zestaw testów."""
    print("\n" + "="*70)
    print("ORCHESTRATOR v2.0 — FULL TEST SUITE")
    print("="*70)
    print("Data: 2026-02-03")
    print("="*70)
    
    tests = [
        ("Test 1: Podstawowy orchestrator", test_1_basic_orchestrator),
        ("Test 2: Orchestrator z embeddings", test_2_orchestrator_with_embeddings),
        ("Test 3: Meta-synteza", test_3_meta_synthesis),
        ("Test 4: Integracja ProjectVector", test_4_projectvector_integration),
        ("Test 5: Przetwarzanie wsadowe", test_5_batch_processing),
        ("Test 6: Embeddings wysokowymiarowe", test_6_high_dimensional_embeddings),
        ("Test 7: Tryb adaptive", test_7_adaptive_mode),
        ("Test 8: Obsługa błędów", test_8_error_handling)
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, "PASSED", None))
        except Exception as e:
            results.append((test_name, "FAILED", str(e)))
            print(f"✗ {test_name} FAILED: {e}")
    
    total_time = (time.time() - start_time) * 1000
    
    # Podsumowanie
    print("\n" + "="*70)
    print("PODSUMOWANIE TESTÓW")
    print("="*70)
    
    passed = sum(1 for _, status, _ in results if status == "PASSED")
    failed = sum(1 for _, status, _ in results if status == "FAILED")
    
    for test_name, status, error in results:
        symbol = "✓" if status == "PASSED" else "✗"
        print(f"{symbol} {test_name}: {status}")
        if error:
            print(f"  Error: {error}")
    
    print("="*70)
    print(f"WYNIK: {passed}/{len(tests)} testów zaliczonych")
    print(f"Czas wykonania: {total_time:.2f} ms")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 WSZYSTKIE TESTY ZALICZONE — SYSTEM OPERACYJNY")
    else:
        print(f"\n⚠️  {failed} testów niezaliczonych — wymagana korekta")
    
    return failed == 0


if __name__ == "__main__":
    success = run_full_test_suite()
    sys.exit(0 if success else 1)
