"""Query generator for AGS.

Generates semantically enriched queries for LongTermGraphManager (LTM).
"""
from typing import List, Dict, Any, Optional

try:
    from CORE.Inference.logos_language_generator import LogosLanguageSynthesizer
except Exception:
    LogosLanguageSynthesizer = None


class QueryGenerator:
    def __init__(self, ltm: Optional[Any] = None, ll_generator: Any = None):
        self.ltm = ltm
        self.ll_generator = ll_generator or (LogosLanguageSynthesizer() if LogosLanguageSynthesizer else None)

    def generate(self, current_state: Any, focus_area: str, depth: int = 3) -> str:
        """Backward-compatible alias to generate_autonomous_query."""
        return self.generate_autonomous_query(current_state, focus_area, depth)

    def generate_autonomous_query(self, current_state: Any, focus_area: str, depth: int = 3) -> str:
        """
        Generate a semantically enriched query string.

        Uses an optional LogosLanguageSynthesizer to create an initial contextual
        query and then iteratively augments it by calling LTM.semantic_search.
        """
        ctx_terms: List[str] = []

        initial_query = (
            f"Current system state: Coherence P={getattr(current_state, 'coherence_p', 'NA')}, "
            f"Autonomy={getattr(current_state, 'autonomy_level', 'NA')}. Focus: {focus_area}."
        )

        # Enrich using logos language generator if available
        try:
            if self.ll_generator and hasattr(self.ll_generator, 'generate_semantic_query'):
                contextual = self.ll_generator.generate_semantic_query(
                    initial_query=initial_query,
                    system_state=current_state,
                    focus_area=focus_area
                )
            else:
                contextual = initial_query
        except Exception:
            contextual = initial_query

        # iterative semantic search augmentation
        relevant_context: List[str] = []
        current_search_query = contextual
        for _ in range(max(1, int(depth))):
            try:
                results = []
                if self.ltm and hasattr(self.ltm, 'semantic_search'):
                    # try common parameter names
                    try:
                        results = self.ltm.semantic_search(current_search_query, k=5) or []
                    except TypeError:
                        try:
                            results = self.ltm.semantic_search(current_search_query, top_k=5) or []
                        except Exception:
                            results = self.ltm.semantic_search(current_search_query) or []

                for r in results:
                    if isinstance(r, dict):
                        content = r.get('metadata', {}).get('content') or r.get('content') or r.get('text')
                    else:
                        content = str(r)
                    if content and content not in relevant_context:
                        relevant_context.append(content)

                if not results:
                    break

                current_search_query = " ".join([contextual] + relevant_context)
            except Exception:
                break

        final_query = f"{contextual}. Relevant context from LTM: {' '.join(relevant_context)}"
        return final_query
