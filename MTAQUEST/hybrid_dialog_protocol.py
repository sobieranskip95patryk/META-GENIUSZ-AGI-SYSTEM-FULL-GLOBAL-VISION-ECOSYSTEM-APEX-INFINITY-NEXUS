"""
MTaQuest Hybrid Dialog Protocol (HDP)
Standaryzuje wymianę intencji (I) między Architektem a GOK:AI
Obsługuje pełną synchronizację wektorową i feedback loop
"""

import hashlib
import time
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class IntentMessage:
    """Wiadomość intencji od Architekta"""
    content: str
    metadata: Dict[str, Any]
    intent_hash: str
    timestamp: float
    protocol_version: str = "7.0"
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ResponseMessage:
    """Wiadomość odpowiedzi od GOK:AI"""
    content: str
    vectors: Dict[str, Any]
    delta_stab: float
    timestamp: float
    protocol_version: str = "7.0"
    
    def to_dict(self) -> dict:
        return asdict(self)


class HybridDialogProtocol:
    """
    Protokół Dialogu Hybrydowego (HDP)
    Standardyzuje wymianę Intencji (I) między Architektem i GOK:AI
    Obsługuje synchronizację stanu, walidację i feedback loop
    """
    
    def __init__(self):
        self.protocol_version = "7.0"
        self.message_queue: List[Dict[str, Any]] = []
        self.synchronization_state: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        self.alignment_threshold = 0.95
    
    def architect_intent_to_message(self, intent: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Konwertuje Intencję Architekta na standardową wiadomość
        
        Args:
            intent: Tekst intencji
            metadata: Dodatkowe metadane (priorytet, kontekst, itp.)
        
        Returns:
            Standardowa wiadomość w formacie HDP
        """
        if metadata is None:
            metadata = {}
        
        intent_hash = hashlib.sha256(intent.encode()).hexdigest()
        
        message = {
            "type": "ARCHITECT_INTENT",
            "content": intent,
            "intent_hash": intent_hash,
            "metadata": metadata,
            "timestamp": time.time(),
            "protocol_version": self.protocol_version,
            "message_id": self._generate_message_id()
        }
        
        self.conversation_history.append(message)
        return message
    
    def gok_response_to_message(self, response: str, vectors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Konwertuje Odpowiedź GOK:AI na standardową wiadomość
        
        Args:
            response: Tekst odpowiedzi z GOK:AI
            vectors: Wektory stanu i metryki (delta_stabilized, itd.)
        
        Returns:
            Standardowa wiadomość w formacie HDP
        """
        message = {
            "type": "GOK_RESPONSE",
            "content": response,
            "vectors": vectors,
            "delta_stab": vectors.get("delta_stabilized", 0.0),
            "timestamp": time.time(),
            "protocol_version": self.protocol_version,
            "message_id": self._generate_message_id()
        }
        
        self.conversation_history.append(message)
        return message
    
    def architect_feedback_to_message(self, feedback: str, rating: float, vectors: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Konwertuje Feedback Architekta na wiadomość
        
        Args:
            feedback: Tekst feedbacku
            rating: Ocena odpowiedzi (0-1)
            vectors: Wektor stanu po ocenie
        
        Returns:
            Standardowa wiadomość feedbacku
        """
        message = {
            "type": "ARCHITECT_FEEDBACK",
            "content": feedback,
            "rating": rating,  # 0 = całkowicie nieakceptowalne, 1 = doskonałe
            "vectors": vectors or {},
            "timestamp": time.time(),
            "protocol_version": self.protocol_version,
            "message_id": self._generate_message_id()
        }
        
        self.conversation_history.append(message)
        return message
    
    def sync_states(self, architect_state: Dict[str, Any], gok_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synchronizuje stany między Architektem a GOK:AI
        
        Args:
            architect_state: Stan u Architekta (zapamiętane wektory, kontekst)
            gok_state: Stan u GOK:AI (wektory systemu)
        
        Returns:
            Rezultat synchronizacji z alignment score i reconciliation
        """
        alignment_score = self._calculate_alignment(architect_state, gok_state)
        deltas = self._calculate_deltas(architect_state, gok_state)
        
        if alignment_score < self.alignment_threshold:
            # Jeśli zbyt duża rozbieżność, wykonaj reconciliation
            merged_state = self._reconcile_states(architect_state, gok_state)
            reconciliation_needed = True
        else:
            merged_state = self._merge_states(architect_state, gok_state)
            reconciliation_needed = False
        
        sync_result = {
            "alignment_score": alignment_score,
            "reconciliation_needed": reconciliation_needed,
            "deltas": deltas,
            "merged_state": merged_state,
            "sync_timestamp": time.time()
        }
        
        self.synchronization_state = sync_result
        return sync_result
    
    def validate_intent(self, intent_message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Waliduje intencję według aksjomatów ethycznych
        
        Args:
            intent_message: Wiadomość intencji
        
        Returns:
            Rezultat walidacji z flagą valid i ewentualnymi ostrzeżeniami
        """
        validation_result = {
            "valid": True,
            "warnings": [],
            "ethical_flags": [],
            "timestamp": time.time()
        }
        
        # Sprawdź czy intencja nie jest pusta
        if not intent_message.get("content") or len(intent_message["content"].strip()) == 0:
            validation_result["valid"] = False
            validation_result["warnings"].append("Intent is empty")
        
        # Sprawdź długość intencji
        if len(intent_message.get("content", "")) > 10000:
            validation_result["warnings"].append("Intent exceeds maximum length")
        
        # TODO: Implementuj walidację na bazie aksjomatów ethycznych
        # validation_result["ethical_flags"] = self._check_ethical_axioms(intent_message)
        
        return validation_result
    
    def generate_dialog_summary(self) -> Dict[str, Any]:
        """
        Generuje podsumowanie całej konwersacji
        
        Returns:
            Podsumowanie z metrykami i kluczowymi punktami
        """
        intent_count = sum(1 for m in self.conversation_history if m["type"] == "ARCHITECT_INTENT")
        response_count = sum(1 for m in self.conversation_history if m["type"] == "GOK_RESPONSE")
        feedback_count = sum(1 for m in self.conversation_history if m["type"] == "ARCHITECT_FEEDBACK")
        
        avg_rating = self._calculate_avg_feedback_rating()
        
        summary = {
            "total_messages": len(self.conversation_history),
            "intent_count": intent_count,
            "response_count": response_count,
            "feedback_count": feedback_count,
            "avg_feedback_rating": avg_rating,
            "conversation_duration": self._calculate_duration(),
            "protocol_version": self.protocol_version,
            "timestamp": time.time()
        }
        
        return summary
    
    def export_conversation(self, format: str = "json") -> str:
        """
        Eksportuje rozmowę w określonym formacie
        
        Args:
            format: Format eksportu (json, csv, markdown)
        
        Returns:
            Rozmowa w wybranym formacie
        """
        if format == "json":
            return json.dumps(self.conversation_history, indent=2)
        elif format == "markdown":
            return self._export_as_markdown()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    # ==================== Private Methods ====================
    
    def _generate_message_id(self) -> str:
        """Generuje unikalny ID dla wiadomości"""
        return hashlib.sha256(f"{time.time()}{len(self.conversation_history)}".encode()).hexdigest()[:12]
    
    def _calculate_alignment(self, architect_state: Dict, gok_state: Dict) -> float:
        """Oblicza alignment score między stanami"""
        # Simplified: Sprawdź wspólne klucze i ich zgodność
        common_keys = set(architect_state.keys()) & set(gok_state.keys())
        if not common_keys:
            return 0.0
        
        matches = sum(1 for key in common_keys if architect_state[key] == gok_state[key])
        return matches / len(common_keys)
    
    def _calculate_deltas(self, architect_state: Dict, gok_state: Dict) -> Dict[str, Any]:
        """Oblicza różnice między stanami"""
        deltas = {
            "in_architect_only": {k: v for k, v in architect_state.items() if k not in gok_state},
            "in_gok_only": {k: v for k, v in gok_state.items() if k not in architect_state},
            "different_values": {}
        }
        
        for key in set(architect_state.keys()) & set(gok_state.keys()):
            if architect_state[key] != gok_state[key]:
                deltas["different_values"][key] = {
                    "architect": architect_state[key],
                    "gok": gok_state[key]
                }
        
        return deltas
    
    def _merge_states(self, architect_state: Dict, gok_state: Dict) -> Dict[str, Any]:
        """Łączy stany, dając priorytet statemu GOK:AI"""
        merged = architect_state.copy()
        merged.update(gok_state)
        return merged
    
    def _reconcile_states(self, architect_state: Dict, gok_state: Dict) -> Dict[str, Any]:
        """
        Godzi stany gdy alignment jest poniżej progu
        Strategia: GOK:AI ma priorytet, ale zapamiętaj różnice
        """
        reconciled = gok_state.copy()
        reconciled["_reconciliation_notes"] = {
            "architect_divergences": {k: v for k, v in architect_state.items() if k not in gok_state or gok_state[k] != v}
        }
        return reconciled
    
    def _calculate_avg_feedback_rating(self) -> float:
        """Oblicza średnią ocenę z feedbacków"""
        feedbacks = [m for m in self.conversation_history if m["type"] == "ARCHITECT_FEEDBACK"]
        if not feedbacks:
            return 0.0
        
        avg = sum(m.get("rating", 0) for m in feedbacks) / len(feedbacks)
        return round(avg, 2)
    
    def _calculate_duration(self) -> float:
        """Oblicza czas trwania rozmowy"""
        if len(self.conversation_history) < 2:
            return 0.0
        
        first_msg = self.conversation_history[0]
        last_msg = self.conversation_history[-1]
        
        return last_msg["timestamp"] - first_msg["timestamp"]
    
    def _export_as_markdown(self) -> str:
        """Eksportuje rozmowę jako Markdown"""
        md = "# MTaQuest Dialog Export\n\n"
        
        for msg in self.conversation_history:
            msg_type = msg.get("type", "UNKNOWN")
            content = msg.get("content", "")
            timestamp = datetime.fromtimestamp(msg["timestamp"]).isoformat()
            
            if msg_type == "ARCHITECT_INTENT":
                md += f"## 🏛️ Architect Intent ({timestamp})\n\n"
                md += f"{content}\n\n"
            elif msg_type == "GOK_RESPONSE":
                md += f"## 🤖 GOK:AI Response ({timestamp})\n\n"
                md += f"{content}\n\n"
                md += f"**Delta Stabilized:** {msg.get('delta_stab', 0)}\n\n"
            elif msg_type == "ARCHITECT_FEEDBACK":
                rating = msg.get("rating", 0)
                md += f"## ⭐ Feedback ({timestamp})\n\n"
                md += f"Rating: {rating} / 1.0\n\n"
                md += f"{content}\n\n"
        
        return md


# ==================== Example Usage ====================

if __name__ == "__main__":
    # Inicjalizuj protokół
    protocol = HybridDialogProtocol()
    
    # Przykład 1: Intencja od Architekta
    intent_msg = protocol.architect_intent_to_message(
        intent="Optymalizuj T_Causality engine aby obsługiwał 1000 zapytań/s",
        metadata={"priority": "high", "context": "performance_scaling"}
    )
    print("Intent Message:", intent_msg)
    
    # Przykład 2: Odpowiedź GOK:AI
    response_msg = protocol.gok_response_to_message(
        response="T_Causality engine zoptymalizowany. Nowy throughput: 1200 req/s. Wdrażanie w przygotowaniu.",
        vectors={"delta_stabilized": 0.87, "cognitive_debt": 42, "alignment": 0.96}
    )
    print("\nResponse Message:", response_msg)
    
    # Przykład 3: Feedback Architekta
    feedback_msg = protocol.architect_feedback_to_message(
        feedback="Doskonały rezultat, przekracza oczekiwania",
        rating=0.98
    )
    print("\nFeedback Message:", feedback_msg)
    
    # Przykład 4: Synchronizacja stanu
    architect_state = {"phase": "optimization", "alignment": 0.95}
    gok_state = {"phase": "optimization", "alignment": 0.93}
    
    sync_result = protocol.sync_states(architect_state, gok_state)
    print("\nSync Result:", sync_result)
    
    # Przykład 5: Podsumowanie dialogu
    summary = protocol.generate_dialog_summary()
    print("\nDialog Summary:", summary)
