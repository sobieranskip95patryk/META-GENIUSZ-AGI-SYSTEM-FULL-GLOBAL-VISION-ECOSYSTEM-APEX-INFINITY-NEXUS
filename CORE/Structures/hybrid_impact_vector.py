# ============================================================================
# HYBRID IMPACT VECTOR (HIV) — Fusion Core Structure
# Łączy ProjectVectors (Global-Vision) + Sense Atoms (AGI_GOK) + EMV (Ethics)
# ============================================================================

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import numpy as np
from enum import Enum


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class ImpactCategory(Enum):
    """Kategorie wpływu projektów na cywilizację"""
    PLANETARY = "PLANETARY"        # Wpływ globalny/planetarny
    CIVILIZATION = "CIVILIZATION"  # Wpływ na strukturę cywilizacji
    ECOSYSTEM = "ECOSYSTEM"        # Wpływ ekologiczny
    ECONOMIC = "ECONOMIC"          # Wpływ ekonomiczny
    SOCIAL = "SOCIAL"              # Wpływ społeczny
    TECHNOLOGICAL = "TECHNOLOGICAL" # Wpływ technologiczny
    EDUCATION = "EDUCATION"        # Wpływ edukacyjny
    HEALTH = "HEALTH"              # Wpływ na zdrowie
    ENERGY = "ENERGY"              # Wpływ energetyczny
    UNKNOWN = "UNKNOWN"            # Nieznany lub mieszany


class RiskLevel(Enum):
    """Poziomy ryzyka przyczynowego"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1
    NONE = 0


class CausalityType(Enum):
    """Typy związków przyczynowych między projektami"""
    SYNERGISTIC = "SYNERGISTIC"      # Projekty się wzmacniają
    COMPETITIVE = "COMPETITIVE"      # Projekty konkurują o zasoby
    NEUTRAL = "NEUTRAL"              # Brak wpływu
    CONFLICTING = "CONFLICTING"      # Projekty się zwalczają
    DEPENDENT = "DEPENDENT"          # Jeden zależy od drugiego


# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

@dataclass
class SenseAtom:
    """
    Sense Atom z AGI_GOK — pojedyncza jednostka logiczna
    Reprezentuje element świadomości systemu
    """
    atom_id: str
    semantic_intent: str           # Intent ekstrakcji (BLOCK, EXPAND, MONITOR)
    weight: float                  # 0.0–1.0 (waga w systmie)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "atom_id": self.atom_id,
            "semantic_intent": self.semantic_intent,
            "weight": self.weight,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


@dataclass
class ProjectMetadata:
    """
    Metadane projektu z Global-Vision
    """
    project_id: str
    project_name: str
    description: str
    creator: str
    category: ImpactCategory
    url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "description": self.description,
            "creator": self.creator,
            "category": self.category.value,
            "url": self.url,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class CausalityLink:
    """
    Link przyczynowy między dwoma projektami
    """
    source_project_id: str
    target_project_id: str
    relationship_type: CausalityType
    strength: float                 # 0.0–1.0 (siła wpływu)
    description: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "source": self.source_project_id,
            "target": self.target_project_id,
            "type": self.relationship_type.value,
            "strength": self.strength,
            "description": self.description
        }


# ============================================================================
# HYBRID IMPACT VECTOR — Główna Klasa
# ============================================================================

@dataclass
class HybridImpactVector:
    """
    HYBRID IMPACT VECTOR (HIV) — fuzja dwóch światów
    
    Łączy:
    1. ProjectVector z Global-Vision (768-dim embedding + metadata)
    2. Sense Atoms z AGI_GOK (logika, intencje, wagi)
    3. Ethical Multi-Vision (EMV) ocena (0.0–1.0)
    4. Causal Graph (związki między projektami)
    
    To jest "DNA" połączonego systemu AGI_GOK + Global-Vision.
    """
    
    # === IDENTITY ===
    vector_id: str                 # Unikalne ID wektora
    
    # === GLOBAL-VISION COMPONENTS ===
    project_metadata: ProjectMetadata  # Metadane projektu
    semantic_embedding: np.ndarray    # 768-dim z OpenAI (Global-Vision)
    embedding_model: str = "openai-text-embedding-3-small"
    
    # === AGI_GOK COMPONENTS ===
    sense_atoms: List[SenseAtom] = field(default_factory=list)  # Logika GOK
    local_score: float = 0.0       # LocalScore z GOK:AI (0–10000)
    
    # === ETHICAL LAYER ===
    ethical_multi_vision_score: float = 0.5  # EMV (0.0–1.0)
    ethical_justification: str = ""
    constraint_violations: List[str] = field(default_factory=list)
    
    # === IMPACT METRICS ===
    gis_score: float = 0.0         # Global Impact Score (0–10000)
    pri_score: float = 0.0         # Planetary Resonance Index (0.0–1.0)
    caf_score: float = 0.0         # Civilization Alignment Factor (0.0–1.0)
    spc_score: float = 0.0         # Synergy Potential Coefficient (0.0–1.0)
    
    # === CAUSALITY ===
    causal_dependencies: List[CausalityLink] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.NONE
    risk_description: str = ""
    
    # === TIMESTAMPS ===
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # === AUDIT TRAIL ===
    audit_log: List[Dict] = field(default_factory=list)
    
    def __post_init__(self):
        """Walidacja po inicjalizacji"""
        if self.semantic_embedding is None:
            raise ValueError("semantic_embedding nie może być None")
        if len(self.semantic_embedding) != 768:
            raise ValueError(f"Embedding musi mieć 768 wymiarów, otrzymano: {len(self.semantic_embedding)}")
        self._audit("vector_created", {"status": "initialized"})
    
    # ========================================================================
    # CORE CALCULATIONS
    # ========================================================================
    
    def calculate_hybrid_priority(self) -> float:
        """
        AUTORSKA FORMUŁA PATRYKA — Synergia logiki, etyki i wpływu
        
        priority = (logic_weight × semantic_match) + (ethics_weight × emv) + (impact_weight × gis_norm)
        
        Gdzie:
        - logic_weight: waga z sense_atoms
        - semantic_match: cosine similarity z embeddings
        - ethics_weight: waga etyki (40%)
        - emv: Ethical Multi-Vision score (0–1)
        - impact_weight: waga wpływu (30%)
        - gis_norm: GIS znormalizowany do 0–1
        
        Returns: float (0–100, gdzie 100 = najwyższy priorytet)
        """
        # Waga logiki z sense_atoms
        logic_weight = sum(atom.weight for atom in self.sense_atoms) / max(len(self.sense_atoms), 1)
        
        # Match semantyczny (placeholder — w praktyce byłby cosine similarity)
        semantic_match = np.mean(np.abs(self.semantic_embedding)) if len(self.sense_atoms) > 0 else 0.5
        semantic_match = min(semantic_match, 1.0)
        
        # Normalizacja GIS (0–10000 → 0–1)
        gis_normalized = min(self.gis_score / 10000.0, 1.0)
        
        # Kombinacja: logika (30%) + etyka (40%) + wpływ (30%)
        priority = (
            (logic_weight * semantic_match * 0.30) +
            (self.ethical_multi_vision_score * 0.40) +
            (gis_normalized * 0.30)
        ) * 100
        
        return round(priority, 2)
    
    
    def calculate_synergy_with(self, other: 'HybridImpactVector') -> float:
        """
        Oblicza synergię między dwoma projektami (wektorami)
        
        Opiera się na:
        1. Cosine similarity embeddings
        2. Komplementarności sense_atoms
        3. Brak konfrontacji etycznej
        
        Returns: float (0.0–1.0, gdzie 1.0 = idealna synergia)
        """
        # 1. Cosine similarity embeddings
        dot_product = np.dot(self.semantic_embedding, other.semantic_embedding)
        norm_self = np.linalg.norm(self.semantic_embedding)
        norm_other = np.linalg.norm(other.semantic_embedding)
        cosine_sim = dot_product / (norm_self * norm_other) if (norm_self * norm_other) > 0 else 0.0
        
        # 2. Komplementarność intencji (sense_atoms)
        intents_self = set(atom.semantic_intent for atom in self.sense_atoms)
        intents_other = set(atom.semantic_intent for atom in other.sense_atoms)
        
        # Jeśli intencje się uzupełniają (np. EXPAND + MONITOR), synergia wyższa
        complementary = 1.0 - (len(intents_self & intents_other) / max(len(intents_self | intents_other), 1))
        
        # 3. Zgodność etyczna
        ethical_alignment = 1.0 - abs(self.ethical_multi_vision_score - other.ethical_multi_vision_score)
        
        # Kombinacja
        synergy = (cosine_sim * 0.5) + (complementary * 0.25) + (ethical_alignment * 0.25)
        
        return round(synergy, 3)
    
    
    def calculate_risk_score(self) -> float:
        """
        Oblicza ryzyko przyczynowe projektu
        
        Bierze pod uwagę:
        1. Liczba i siła causal_dependencies
        2. Constraint violations
        3. Risk level
        4. Odwrotność EMV (niska etyka = wyższe ryzyko)
        
        Returns: float (0–1, gdzie 1 = maksymalne ryzyko)
        """
        # 1. Ryzyko z causal dependencies
        dependency_risk = 0.0
        for link in self.causal_dependencies:
            if link.relationship_type == CausalityType.CONFLICTING:
                dependency_risk += link.strength * 0.5
            elif link.relationship_type == CausalityType.COMPETITIVE:
                dependency_risk += link.strength * 0.3
        
        dependency_risk = min(dependency_risk / max(len(self.causal_dependencies), 1), 1.0)
        
        # 2. Constraint violations
        violation_risk = min(len(self.constraint_violations) * 0.1, 1.0)
        
        # 3. Risk level
        risk_level_score = self.risk_level.value / 5.0
        
        # 4. Odwrotność EMV
        emv_risk = 1.0 - self.ethical_multi_vision_score
        
        # Kombinacja
        total_risk = (
            (dependency_risk * 0.30) +
            (violation_risk * 0.20) +
            (risk_level_score * 0.30) +
            (emv_risk * 0.20)
        )
        
        return round(min(total_risk, 1.0), 3)
    
    
    def verify_ethical_alignment(self) -> Tuple[bool, str]:
        """
        Weryfikuje, czy projekt spełnia minimalne standardy etyczne
        
        Returns:
            Tuple[bool, str] — (is_aligned, justification)
        """
        issues = []
        
        # 1. EMV musi być > 0.3
        if self.ethical_multi_vision_score < 0.3:
            issues.append(f"EMV score ({self.ethical_multi_vision_score}) poniżej minimum 0.3")
        
        # 2. Constraint violations muszą być wyjaśnione
        if len(self.constraint_violations) > 0 and not self.ethical_justification:
            issues.append("Naruszenia constraints nie mają uzasadnienia")
        
        # 3. Risk level nie może być CRITICAL bez EMV > 0.7
        if self.risk_level == RiskLevel.CRITICAL and self.ethical_multi_vision_score < 0.7:
            issues.append("Projekt CRITICAL risk bez wystarczającej EMV")
        
        # 4. GIS < 4000 nie powinien być finansowany
        if self.gis_score < 4000 and self.calculate_hybrid_priority() > 50:
            issues.append("Niska GIS score vs wysoki priorytet — sprzeczność")
        
        is_aligned = len(issues) == 0
        justification = "; ".join(issues) if issues else "Zaakceptowano — projekt spełnia kryteria etyczne"
        
        return is_aligned, justification
    
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def add_sense_atom(self, atom: SenseAtom) -> None:
        """Dodaj sense atom (logika z AGI_GOK)"""
        self.sense_atoms.append(atom)
        self._audit("sense_atom_added", {"atom_id": atom.atom_id})
    
    
    def add_causal_link(self, link: CausalityLink) -> None:
        """Dodaj link przyczynowy do innego projektu"""
        self.causal_dependencies.append(link)
        self._audit("causal_link_added", {
            "source": link.source_project_id,
            "target": link.target_project_id,
            "type": link.relationship_type.value
        })
    
    
    def add_constraint_violation(self, violation: str) -> None:
        """Zanotuj naruszenie constraint'u"""
        self.constraint_violations.append(violation)
        self._audit("constraint_violation_added", {"violation": violation})
    
    
    def _audit(self, event: str, details: Dict) -> None:
        """Wewnętrzna funkcja audytu"""
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details
        })
        self.updated_at = datetime.now().isoformat()
    
    
    def to_dict(self) -> Dict:
        """Serializacja do słownika (do JSON)"""
        return {
            "vector_id": self.vector_id,
            "project_metadata": self.project_metadata.to_dict(),
            "semantic_embedding_dim": len(self.semantic_embedding),
            "embedding_model": self.embedding_model,
            "sense_atoms": [atom.to_dict() for atom in self.sense_atoms],
            "local_score": self.local_score,
            "ethical_multi_vision_score": self.ethical_multi_vision_score,
            "ethical_justification": self.ethical_justification,
            "constraint_violations": self.constraint_violations,
            "gis_score": self.gis_score,
            "pri_score": self.pri_score,
            "caf_score": self.caf_score,
            "spc_score": self.spc_score,
            "causal_dependencies": [link.to_dict() for link in self.causal_dependencies],
            "risk_level": self.risk_level.name,
            "risk_description": self.risk_description,
            "hybrid_priority": self.calculate_hybrid_priority(),
            "risk_score": self.calculate_risk_score(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "audit_log_entries": len(self.audit_log)
        }
    
    
    def to_json(self, indent: int = 2) -> str:
        """Serializacja do JSON string'u"""
        # Konwersja numpy array do listy
        data = self.to_dict()
        data["semantic_embedding"] = self.semantic_embedding.tolist() if isinstance(self.semantic_embedding, np.ndarray) else self.semantic_embedding
        return json.dumps(data, indent=indent, default=str)
    
    
    def __repr__(self) -> str:
        return (
            f"HybridImpactVector(id={self.vector_id}, "
            f"project={self.project_metadata.project_name}, "
            f"gis={self.gis_score:.0f}, "
            f"priority={self.calculate_hybrid_priority():.1f}, "
            f"risk={self.risk_level.name})"
        )


# ============================================================================
# FACTORY & UTILITIES
# ============================================================================

class HybridImpactVectorFactory:
    """
    Factory do tworzenia HybridImpactVectors z dostępnych danych
    """
    
    @staticmethod
    def from_global_vision_data(
        project_id: str,
        project_name: str,
        description: str,
        embedding: np.ndarray,
        creator: str = "unknown",
        category: ImpactCategory = ImpactCategory.UNKNOWN
    ) -> HybridImpactVector:
        """
        Tworzy HIV z danych Global-Vision
        """
        metadata = ProjectMetadata(
            project_id=project_id,
            project_name=project_name,
            description=description,
            creator=creator,
            category=category
        )
        
        return HybridImpactVector(
            vector_id=f"{project_id}_hiv_{datetime.now().timestamp()}",
            project_metadata=metadata,
            semantic_embedding=embedding
        )
    
    
    @staticmethod
    def from_agi_gok_data(
        gis_score: float,
        local_score: float,
        pri: float,
        caf: float,
        spc: float,
        project_metadata: ProjectMetadata,
        embedding: np.ndarray
    ) -> HybridImpactVector:
        """
        Tworzy HIV z danych AGI_GOK (GlobalVision Analyzer)
        """
        hiv = HybridImpactVector(
            vector_id=f"{project_metadata.project_id}_hiv_{datetime.now().timestamp()}",
            project_metadata=project_metadata,
            semantic_embedding=embedding,
            local_score=local_score,
            gis_score=gis_score,
            pri_score=pri,
            caf_score=caf,
            spc_score=spc
        )
        
        return hiv


# ============================================================================
# VALIDATION & DIAGNOSTICS
# ============================================================================

def validate_hybrid_impact_vector(hiv: HybridImpactVector) -> Tuple[bool, List[str]]:
    """
    Waliduje HybridImpactVector pod kątem integralności
    
    Returns:
        Tuple[bool, List[str]] — (is_valid, errors)
    """
    errors = []
    
    # 1. Embedding
    if hiv.semantic_embedding is None:
        errors.append("Brak semantic_embedding")
    elif len(hiv.semantic_embedding) != 768:
        errors.append(f"Zły rozmiar embedding: {len(hiv.semantic_embedding)} != 768")
    
    # 2. Metadata
    if not hiv.project_metadata.project_id:
        errors.append("Brak project_id")
    if not hiv.project_metadata.project_name:
        errors.append("Brak project_name")
    
    # 3. Scores
    if not (0 <= hiv.gis_score <= 10000):
        errors.append(f"GIS score poza zakresem: {hiv.gis_score}")
    if not (0 <= hiv.pri_score <= 1.0):
        errors.append(f"PRI score poza zakresem: {hiv.pri_score}")
    if not (0 <= hiv.caf_score <= 1.0):
        errors.append(f"CAF score poza zakresem: {hiv.caf_score}")
    if not (0 <= hiv.spc_score <= 1.0):
        errors.append(f"SPC score poza zakresem: {hiv.spc_score}")
    if not (0 <= hiv.ethical_multi_vision_score <= 1.0):
        errors.append(f"EMV score poza zakresem: {hiv.ethical_multi_vision_score}")
    
    is_valid = len(errors) == 0
    
    return is_valid, errors


if __name__ == "__main__":
    # ========================================================================
    # DEMO: Tworzenie HybridImpactVector
    # ========================================================================
    print("=" * 80)
    print("HYBRID IMPACT VECTOR — Demo Implementacji")
    print("=" * 80)
    
    # 1. Tworzenie embeddings (symulacja)
    np.random.seed(42)
    embedding = np.random.randn(768).astype(np.float32)
    embedding = embedding / np.linalg.norm(embedding)  # Normalizacja
    
    # 2. Tworzenie ProjectMetadata
    metadata = ProjectMetadata(
        project_id="PROJECT_001",
        project_name="Cosmic Education Platform",
        description="Global platform for space education and astronomy",
        creator="Patryk Sobierański",
        category=ImpactCategory.EDUCATION,
        tags=["education", "space", "global", "science"]
    )
    
    # 3. Tworzenie HybridImpactVector
    hiv = HybridImpactVector(
        vector_id="HIV_PROJECT_001_001",
        project_metadata=metadata,
        semantic_embedding=embedding,
        local_score=1751.45,
        gis_score=8760.73,
        pri_score=0.92,
        caf_score=0.88,
        spc_score=0.75,
        ethical_multi_vision_score=0.92,
        ethical_justification="Projekt wspiera edukację i świadomość planetarną bez negatywnych skutków ubocznych",
        risk_level=RiskLevel.MINIMAL
    )
    
    # 4. Dodanie sense_atoms (logika z AGI_GOK)
    atom1 = SenseAtom(
        atom_id="ATOM_001",
        semantic_intent="EXPAND",
        weight=0.95,
        metadata={"reasoning": "Projekt ma wysoce pozytywny wpływ planetarny"}
    )
    atom2 = SenseAtom(
        atom_id="ATOM_002",
        semantic_intent="MONITOR",
        weight=0.85,
        metadata={"reasoning": "Wymagać ciągłego badania wpływu edukacyjnego"}
    )
    
    hiv.add_sense_atom(atom1)
    hiv.add_sense_atom(atom2)
    
    # 5. Obliczenia
    priority = hiv.calculate_hybrid_priority()
    risk_score = hiv.calculate_risk_score()
    is_aligned, justification = hiv.verify_ethical_alignment()
    
    # 6. Wyniki
    print(f"\n✅ HybridImpactVector created successfully")
    print(f"\n📊 Project: {metadata.project_name}")
    print(f"   Category: {metadata.category.value}")
    print(f"   Creator: {metadata.creator}")
    print(f"\n📈 Impact Metrics:")
    print(f"   GIS Score: {hiv.gis_score:.2f} / 10000")
    print(f"   PRI Score: {hiv.pri_score:.2f} / 1.0")
    print(f"   CAF Score: {hiv.caf_score:.2f} / 1.0")
    print(f"   SPC Score: {hiv.spc_score:.2f} / 1.0")
    print(f"   Local Score: {hiv.local_score:.2f} / 10000")
    
    print(f"\n🧠 Logic & Ethics:")
    print(f"   Sense Atoms: {len(hiv.sense_atoms)}")
    print(f"   EMV Score: {hiv.ethical_multi_vision_score:.2f} / 1.0")
    print(f"   Ethical Alignment: {is_aligned} — {justification}")
    
    print(f"\n🎯 Calculated Metrics:")
    print(f"   Hybrid Priority: {priority:.2f} / 100.0")
    print(f"   Risk Score: {risk_score:.3f} / 1.0")
    print(f"   Risk Level: {hiv.risk_level.name}")
    
    print(f"\n📋 Vector Summary:")
    print(f"   Vector ID: {hiv.vector_id}")
    print(f"   Created: {hiv.created_at}")
    print(f"   Audit Entries: {len(hiv.audit_log)}")
    
    # 7. Walidacja
    is_valid, errors = validate_hybrid_impact_vector(hiv)
    print(f"\n✔️ Validation: {'PASSED' if is_valid else 'FAILED'}")
    if errors:
        for error in errors:
            print(f"   ⚠️  {error}")
    
    # 8. JSON Export
    print(f"\n📄 JSON Export (fragment):")
    json_data = hiv.to_json()
    print(json_data[:500] + "...\n")
    
    print("=" * 80)
    print("Demo Complete ✅")
    print("=" * 80)
