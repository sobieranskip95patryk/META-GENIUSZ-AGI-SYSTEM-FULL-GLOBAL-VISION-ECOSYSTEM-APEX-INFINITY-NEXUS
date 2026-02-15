# ============================================================================
# MIGRATION SCRIPT: Global-Vision v1.0 → HybridImpactVector
# ============================================================================

"""
Ten skrypt migruje dane z Global-Vision v1.0 do HybridImpactVectors.

Proces:
1. Wczytanie projektów z GV v1.0 (JSON/embeddings)
2. Przetworzenie przez GlobalVisionAnalyzer
3. Transformacja do HybridImpactVectors
4. Zapis do pliku audit-ready

Uruchomienie:
    python CORE/Structures/migration_gv_to_hiv.py \
        --gv-data /path/to/gv_projects.json \
        --output /path/to/hiv_portfolio.json
"""

import json
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
from pathlib import Path

# Importy z naszych modułów
from CORE.Structures.hybrid_impact_vector import (
    HybridImpactVector,
    ProjectMetadata,
    SenseAtom,
    CausalityLink,
    ImpactCategory,
    RiskLevel,
    CausalityType,
    HybridImpactVectorFactory,
    validate_hybrid_impact_vector
)
from CORE.Inference.global_vision_analyzer import GlobalVisionAnalyzer


# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# MIGRATION ENGINE
# ============================================================================

class GlobalVisionToHIVMigration:
    """
    Engine do migracji danych z Global-Vision v1.0 na HybridImpactVectors
    """
    
    def __init__(self):
        """Inicjalizacja"""
        self.analyzer = GlobalVisionAnalyzer()
        self.migration_log: List[Dict] = []
        self.hiv_portfolio: List[HybridImpactVector] = []
        self.errors: List[str] = []
        logger.info("Migration Engine initialized")
    
    
    def load_gv_projects(self, gv_json_path: str) -> List[Dict]:
        """
        Wczytanie projektów z Global-Vision JSON
        
        Oczekiwany format:
        {
          "projects": [
            {
              "project_id": "...",
              "project_name": "...",
              "description": "...",
              "creator": "...",
              "embedding": [...],  // 768-dim array
              "metadata": {...}
            }
          ]
        }
        """
        try:
            with open(gv_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            projects = data.get("projects", [])
            logger.info(f"Loaded {len(projects)} projects from {gv_json_path}")
            return projects
        
        except Exception as e:
            error_msg = f"Failed to load GV projects: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return []
    
    
    def migrate_project_to_hiv(
        self,
        gv_project: Dict,
        index: int = 0
    ) -> Optional[HybridImpactVector]:
        """
        Migruje jeden projekt z Global-Vision do HybridImpactVector
        
        Proces:
        1. Ekstrakcja danych z GV
        2. Obliczenie GIS (GlobalVisionAnalyzer)
        3. Tworzenie HIV
        4. Dodanie sense_atoms
        5. Weryfikacja etyczna
        """
        try:
            # === STEP 1: Ekstrakcja danych z GV ===
            project_id = gv_project.get("project_id", f"GV_PROJECT_{index}")
            project_name = gv_project.get("project_name", "Unknown Project")
            description = gv_project.get("description", "")
            creator = gv_project.get("creator", "unknown")
            
            # Embedding (768-dim)
            embedding_data = gv_project.get("embedding", None)
            if embedding_data is None:
                raise ValueError(f"Project {project_id} has no embedding data")
            
            embedding = np.array(embedding_data, dtype=np.float32)
            if embedding.shape[0] != 768:
                # Try to normalize if wrong size
                embedding = embedding[:768] if len(embedding) > 768 else np.pad(embedding, (0, 768 - len(embedding)))
            
            # Normalizacja embeddings
            embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
            
            # Metadata z GV
            gv_metadata = gv_project.get("metadata", {})
            
            # === STEP 2: Obliczenie GIS (GlobalVisionAnalyzer) ===
            # Ekstrahowanie lokalnych wyników (jeśli dostępne)
            local_score = gv_project.get("local_score", 0.0)
            pri = gv_project.get("pri", 0.0)
            caf = gv_project.get("caf", 0.0)
            spc = gv_project.get("spc", 0.0)
            
            # Jeśli brakuje, obliczamy na podstawie embeddings + metadata
            if local_score == 0.0:
                # Heurystyka: słowa kluczowe w opisie vs embedding magnitude
                keyword_score = self._score_from_keywords(description)
                local_score = keyword_score * 1000  # Scale to 0–10000
            
            # Obliczenie GIS przez analyzer
            metrics = self.analyzer.calculate_gis(
                local_score=local_score,
                pri=pri,
                caf=caf,
                spc=spc,
                project_name=project_name
            )
            
            # === STEP 3: Kategoria Wpływu ===
            category = self._infer_impact_category(description, gv_metadata.get("category", ""))
            
            # === STEP 4: Tworzenie ProjectMetadata ===
            project_metadata = ProjectMetadata(
                project_id=project_id,
                project_name=project_name,
                description=description,
                creator=creator,
                category=category,
                url=gv_metadata.get("url"),
                tags=gv_metadata.get("tags", []),
                created_at=gv_metadata.get("created_at", datetime.now().isoformat()),
                updated_at=datetime.now().isoformat()
            )
            
            # === STEP 5: Tworzenie HybridImpactVector ===
            hiv = HybridImpactVectorFactory.from_agi_gok_data(
                gis_score=metrics.gis,
                local_score=local_score,
                pri=pri,
                caf=caf,
                spc=spc,
                project_metadata=project_metadata,
                embedding=embedding
            )
            
            # === STEP 6: Dodanie sense_atoms (logika) ===
            # Automatyczne generowanie sense_atoms na podstawie GIS
            sense_atoms = self._generate_sense_atoms(metrics.gis, project_name)
            for atom in sense_atoms:
                hiv.add_sense_atom(atom)
            
            # === STEP 7: Ocena etyczna (EMV) ===
            emv_score = self._calculate_emv(description, metrics.gis, pri, caf)
            hiv.ethical_multi_vision_score = emv_score
            hiv.ethical_justification = f"EMV calculated from project description and impact metrics"
            
            # === STEP 8: Ryzyka ===
            risk_level = self._infer_risk_level(metrics.gis, emv_score)
            hiv.risk_level = risk_level
            hiv.risk_description = f"Inferred from GIS={metrics.gis:.0f}, EMV={emv_score:.2f}"
            
            # === STEP 9: Weryfikacja ===
            is_valid, errors = validate_hybrid_impact_vector(hiv)
            if not is_valid:
                logger.warning(f"Project {project_id} validation issues: {errors}")
            
            logger.info(f"✓ Migrated {project_id} → {hiv.vector_id}")
            
            return hiv
        
        except Exception as e:
            error_msg = f"Migration failed for project {gv_project.get('project_id', f'index_{index}')}: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return None
    
    
    def migrate_all_projects(self, gv_projects: List[Dict]) -> List[HybridImpactVector]:
        """
        Migruje wszystkie projekty z Global-Vision
        
        Returns: List[HybridImpactVector]
        """
        logger.info(f"Starting migration of {len(gv_projects)} projects...")
        
        hivs = []
        for index, gv_project in enumerate(gv_projects):
            hiv = self.migrate_project_to_hiv(gv_project, index)
            if hiv:
                hivs.append(hiv)
        
        self.hiv_portfolio = hivs
        logger.info(f"Migration complete: {len(hivs)} projects successfully migrated")
        
        return hivs
    
    
    def calculate_portfolio_synergies(self) -> Dict[str, List[Tuple[str, float]]]:
        """
        Oblicza synergię między wszystkimi projektami w portfolio
        
        Returns:
            Dict[project_id, List[(other_project_id, synergy_score)]]
        """
        logger.info("Calculating portfolio synergies...")
        
        synergies = {}
        for i, hiv1 in enumerate(self.hiv_portfolio):
            synergies[hiv1.vector_id] = []
            for j, hiv2 in enumerate(self.hiv_portfolio):
                if i != j:
                    synergy = hiv1.calculate_synergy_with(hiv2)
                    synergies[hiv1.vector_id].append((hiv2.vector_id, synergy))
            
            # Sort by synergy score
            synergies[hiv1.vector_id].sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"Calculated synergies for {len(self.hiv_portfolio)} projects")
        
        return synergies
    
    
    def export_to_json(self, output_path: str, include_embeddings: bool = False) -> bool:
        """
        Eksportuje migrowane HIVs do JSON
        
        Args:
            output_path: Ścieżka do pliku wyjściowego
            include_embeddings: Czy inkludować 768-dim embeddings (dużo danych!)
        """
        try:
            portfolio_data = []
            for hiv in self.hiv_portfolio:
                hiv_dict = hiv.to_dict()
                
                # Opcjonalnie: dodaj embeddings
                if include_embeddings:
                    hiv_dict["semantic_embedding"] = hiv.semantic_embedding.tolist()
                
                portfolio_data.append(hiv_dict)
            
            # Metadane migracji
            migration_metadata = {
                "migration_timestamp": datetime.now().isoformat(),
                "source": "Global-Vision v1.0",
                "target": "HybridImpactVector",
                "total_projects": len(self.hiv_portfolio),
                "errors_count": len(self.errors),
                "include_embeddings": include_embeddings
            }
            
            output = {
                "metadata": migration_metadata,
                "portfolio": portfolio_data,
                "migration_errors": self.errors
            }
            
            # Zapis do JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, default=str)
            
            logger.info(f"✓ Portfolio exported to {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return False
    
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _score_from_keywords(self, text: str) -> float:
        """
        Heurystyka: Obliczenie wyniku na podstawie słów kluczowych
        0.0–1.0
        """
        high_impact_keywords = [
            "planetary", "global", "worldwide", "civilization",
            "education", "cure", "renewable", "sustainability",
            "breakthrough", "revolutionary", "transformative"
        ]
        
        text_lower = text.lower()
        count = sum(1 for kw in high_impact_keywords if kw in text_lower)
        
        return min(count / len(high_impact_keywords), 1.0)
    
    
    def _infer_impact_category(self, description: str, metadata_category: str) -> ImpactCategory:
        """
        Wnioskowanie kategorii wpływu z opisu i metadanych
        """
        text = (description + " " + metadata_category).lower()
        
        if any(kw in text for kw in ["education", "learn", "school", "university"]):
            return ImpactCategory.EDUCATION
        elif any(kw in text for kw in ["tech", "technology", "ai", "quantum", "chip"]):
            return ImpactCategory.TECHNOLOGICAL
        elif any(kw in text for kw in ["ecology", "climate", "carbon", "green", "forest", "ocean"]):
            return ImpactCategory.ECOSYSTEM
        elif any(kw in text for kw in ["health", "medicine", "cure", "disease", "therapy"]):
            return ImpactCategory.HEALTH
        elif any(kw in text for kw in ["energy", "power", "renewable", "solar", "wind"]):
            return ImpactCategory.ENERGY
        elif any(kw in text for kw in ["economy", "finance", "business", "market"]):
            return ImpactCategory.ECONOMIC
        elif any(kw in text for kw in ["social", "community", "equality", "justice"]):
            return ImpactCategory.SOCIAL
        else:
            return ImpactCategory.UNKNOWN
    
    
    def _generate_sense_atoms(self, gis_score: float, project_name: str) -> List[SenseAtom]:
        """
        Automatyczne generowanie sense_atoms na podstawie GIS
        """
        atoms = []
        
        # Atom 1: Intent (EXPAND / MONITOR / BLOCK)
        if gis_score >= 8500:
            intent = "EXPAND"
            weight = 0.95
        elif gis_score >= 6500:
            intent = "MONITOR"
            weight = 0.85
        elif gis_score >= 4000:
            intent = "MONITOR"
            weight = 0.70
        else:
            intent = "BLOCK"
            weight = 0.50
        
        atom1 = SenseAtom(
            atom_id=f"ATOM_{project_name.replace(' ', '_').upper()}_INTENT",
            semantic_intent=intent,
            weight=weight,
            metadata={
                "gis_score": gis_score,
                "reasoning": f"Auto-generated from GIS score"
            }
        )
        atoms.append(atom1)
        
        # Atom 2: Caution (jeśli ryzyko)
        if gis_score < 5000:
            atom2 = SenseAtom(
                atom_id=f"ATOM_{project_name.replace(' ', '_').upper()}_CAUTION",
                semantic_intent="MONITOR",
                weight=0.80,
                metadata={
                    "gis_score": gis_score,
                    "reasoning": "Low GIS score — requires monitoring"
                }
            )
            atoms.append(atom2)
        
        return atoms
    
    
    def _calculate_emv(self, description: str, gis: float, pri: float, caf: float) -> float:
        """
        Obliczenie Ethical Multi-Vision Score
        
        EMV = (keyword_ethics × 0.30) + (gis_aligned × 0.40) + (pri_weight × 0.30)
        """
        # 1. Keywords etyczne w opisie
        ethical_keywords = ["sustainable", "ethical", "responsible", "safe", "transparent"]
        keyword_score = sum(1 for kw in ethical_keywords if kw in description.lower()) / len(ethical_keywords)
        
        # 2. Wyrównanie GIS (wyższy GIS = większa odpowiedzialność)
        gis_aligned = min(gis / 10000, 1.0)
        
        # 3. Waga Planetary Resonance
        pri_weight = pri
        
        emv = (keyword_score * 0.30) + (gis_aligned * 0.40) + (pri_weight * 0.30)
        
        return min(max(emv, 0.0), 1.0)
    
    
    def _infer_risk_level(self, gis: float, emv: float) -> RiskLevel:
        """
        Wnioskowanie Risk Level z GIS i EMV
        """
        if gis >= 8500 and emv >= 0.8:
            return RiskLevel.NONE
        elif gis >= 6500 and emv >= 0.6:
            return RiskLevel.MINIMAL
        elif gis >= 4000 and emv >= 0.4:
            return RiskLevel.LOW
        elif gis >= 2000:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH
    
    
    def print_summary(self):
        """Drukuje podsumowanie migracji"""
        print("\n" + "="*80)
        print("MIGRATION SUMMARY")
        print("="*80)
        
        print(f"\n✓ Total Projects Migrated: {len(self.hiv_portfolio)}")
        print(f"⚠️  Errors: {len(self.errors)}")
        
        if self.hiv_portfolio:
            gis_scores = [hiv.gis_score for hiv in self.hiv_portfolio]
            priorities = [hiv.calculate_hybrid_priority() for hiv in self.hiv_portfolio]
            
            print(f"\n📊 GIS Metrics:")
            print(f"   Average: {np.mean(gis_scores):.0f}")
            print(f"   Min: {np.min(gis_scores):.0f}")
            print(f"   Max: {np.max(gis_scores):.0f}")
            
            print(f"\n🎯 Priority Metrics:")
            print(f"   Average: {np.mean(priorities):.1f}")
            print(f"   Min: {np.min(priorities):.1f}")
            print(f"   Max: {np.max(priorities):.1f}")
            
            # Top 3 projects
            top_3_indices = np.argsort(priorities)[-3:]
            print(f"\n🏆 Top 3 Projects:")
            for idx in reversed(top_3_indices):
                hiv = self.hiv_portfolio[idx]
                print(f"   {idx+1}. {hiv.project_metadata.project_name} (Priority: {priorities[idx]:.1f}, GIS: {hiv.gis_score:.0f})")
        
        if self.errors:
            print(f"\n❌ Errors:")
            for error in self.errors[:5]:  # Show first 5
                print(f"   - {error}")
        
        print("\n" + "="*80 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate Global-Vision v1.0 projects to HybridImpactVectors")
    parser.add_argument("--gv-data", type=str, default="gv_projects_sample.json", help="Path to GV projects JSON")
    parser.add_argument("--output", type=str, default="hiv_portfolio_migrated.json", help="Output path")
    parser.add_argument("--include-embeddings", action="store_true", help="Include 768-dim embeddings in output")
    
    args = parser.parse_args()
    
    # === RUN MIGRATION ===
    engine = GlobalVisionToHIVMigration()
    
    # 1. Wczytanie projektów
    gv_projects = engine.load_gv_projects(args.gv_data)
    
    if gv_projects:
        # 2. Migracja
        hivs = engine.migrate_all_projects(gv_projects)
        
        # 3. Analiza synergii
        synergies = engine.calculate_portfolio_synergies()
        
        # 4. Eksport
        success = engine.export_to_json(args.output, include_embeddings=args.include_embeddings)
        
        # 5. Podsumowanie
        engine.print_summary()
        
        if success:
            print(f"✅ Migration completed! Data exported to: {args.output}")
        else:
            print("❌ Export failed")
    else:
        print(f"❌ No projects loaded from {args.gv_data}")
