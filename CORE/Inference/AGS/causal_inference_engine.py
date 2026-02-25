"""Causal inference helpers for AGS.

Provides simple hypothesis generation and lightweight proof aggregation
based on LTM search results and heuristic scoring.
"""
from typing import List, Dict, Any, Optional

class CausalInferenceEngine:
    def __init__(self, ltm: Optional[Any] = None, ll_generator: Any = None):
        self.ltm = ltm
        self.ll_generator = ll_generator

    def generate_hypothesis(self, current_state: Any, query_results: List[Dict[str, Any]]) -> str:
        """Synthesize a short causal hypothesis from query results."""
        # Simple heuristic: aggregate top concept names
        tops = []
        for r in (query_results or [])[:5]:
            node = r.get('node_id') or r.get('id') or r.get('node') or r.get('label')
            if node:
                tops.append(str(node))
        if not tops:
            return "Increase evidence for causal link in focus area"
        return " -> ".join(tops)

    # New API expected by AutonomousGoalSystem
    def generate_causal_hypothesis(self, problem_statement: str, context: List[str], current_state: Any) -> str:
        """
        Produce a candidate causal hypothesis given a problem statement, an
        initial list of contextual facts (from LTM) and the current system state.
        """
        # Simple composition
        composed_context = " ".join(context or [])
        full_input = f"Problem: {problem_statement}. Context: {composed_context}. State coherence={getattr(current_state, 'coherence_p', 'NA')}"

        # Prefer a LogosLanguageSynthesizer if LLG is available on LTM or via external
        hypothesis = None
        try:
            # use provided ll_generator if available
            llg = getattr(self, 'll_generator', None)
            if llg and hasattr(llg, 'generate_causal_hypothesis'):
                hypothesis = llg.generate_causal_hypothesis(problem_context=full_input, system_state=current_state)
        except Exception:
            hypothesis = None

        # fallback heuristic
        if not hypothesis:
            low_coherence = getattr(current_state, 'coherence_p', 1.0) < 0.9
            if low_coherence and any('degrad' in s.lower() or 'anomal' in s.lower() for s in (context or [])):
                hypothesis = (
                    f"Hypothesis: Integration anomalies and inconsistent data inflows are causally linked to coherence drop (P={current_state.coherence_p:.2f})."
                )
            else:
                snippet = (composed_context[:300] + '...') if composed_context else ''
                hypothesis = f"Hypothesis: No single dominant cause identified. Context sample: {snippet}"

        # Enrich hypothesis via LTM if possible
        try:
            if self.ltm and hasattr(self.ltm, 'semantic_search'):
                enrich = self.ltm.semantic_search(hypothesis, k=3) or []
                facts = [r.get('metadata', {}).get('content') or r.get('content') for r in enrich if isinstance(r, dict)]
                if facts:
                    hypothesis += f" (Relevant LTM insights: {'; '.join([f for f in facts if f])})"
        except Exception:
            pass

        return hypothesis

    def generate_causal_proof(self, causal_hypothesis: str, query_results: List[Dict[str, Any]], current_state: Any) -> Dict[str, Any]:
        """
        Verify the `causal_hypothesis` by aggregating evidence from `query_results`
        and performing depth-limited semantic search in the LTM. Optionally uses
        `ll_generator.verify_causal_proof` for semantic analysis.
        """
        return self.generate_causal_proof_full(causal_hypothesis, query_results, current_state, depth=2)

    def generate_causal_proof_full(self, causal_hypothesis: str, query_results: List[Dict[str, Any]], current_state: Any, depth: int = 2) -> Dict[str, Any]:
        """
        Full proof generation routine. Returns dict with keys:
        - is_proven: bool
        - supporting_facts: List[str]
        - contradicting_facts: List[str]
        - knowledge_gaps: List[str]
        """
        supporting_facts: List[str] = []
        contradicting_facts: List[str] = []
        knowledge_gaps: List[str] = []

        # Normalize incoming query_results into text facts
        proof_context: List[str] = []
        for r in (query_results or []):
            if isinstance(r, dict):
                content = r.get('metadata', {}).get('content') or r.get('content') or r.get('text')
            else:
                content = str(r)
            if content:
                proof_context.append(content)

        # Iterative semantic search to gather additional evidence
        current_search_query = causal_hypothesis + " " + " ".join(proof_context)
        for _ in range(max(0, int(depth))):
            try:
                if not self.ltm or not hasattr(self.ltm, 'semantic_search'):
                    break
                # try different parameter names
                try:
                    additional = self.ltm.semantic_search(current_search_query, k=5) or []
                except TypeError:
                    try:
                        additional = self.ltm.semantic_search(current_search_query, top_k=5) or []
                    except Exception:
                        additional = self.ltm.semantic_search(current_search_query) or []

                if not additional:
                    break

                new_found = False
                for r in additional:
                    if isinstance(r, dict):
                        content = r.get('metadata', {}).get('content') or r.get('content') or r.get('text')
                    else:
                        content = str(r)
                    if content and content not in proof_context:
                        proof_context.append(content)
                        new_found = True
                if not new_found:
                    break
                current_search_query += " " + " ".join(proof_context[-5:])
            except Exception:
                break

        # If a logos language generator with verification capability exists, use it
        llg_result = None
        try:
            if self.ll_generator and hasattr(self.ll_generator, 'verify_causal_proof'):
                llg_input = {
                    'hypothesis': causal_hypothesis,
                    'context_facts': proof_context,
                    'system_state': current_state
                }
                llg_result = self.ll_generator.verify_causal_proof(llg_input)
        except Exception:
            llg_result = None

        if llg_result and isinstance(llg_result, dict):
            is_proven = bool(llg_result.get('is_consistent'))
            supporting_facts = llg_result.get('supporting', []) or []
            contradicting_facts = llg_result.get('contradicting', []) or []
            knowledge_gaps = llg_result.get('gaps', []) or []
        else:
            # Fallback heuristic classification from proof_context
            for fact in proof_context:
                lf = fact.lower()
                if any(k in lf for k in ['confirm', 'confirmed', 'evidence', 'supports', 'supports that', 'causes', 'leads to']):
                    supporting_facts.append(fact)
                if any(k in lf for k in ['not', 'no', 'does not', 'contradict', 'contradicted', 'fails to']):
                    contradicting_facts.append(fact)
                if any(k in lf for k in ['missing', 'no direct evidence', 'unknown', 'insufficient']):
                    knowledge_gaps.append(fact)

            # Determine proof status conservatively
            if supporting_facts and not contradicting_facts:
                is_proven = True
            else:
                is_proven = False

            # If nothing found at all, record a generic knowledge gap
            if not supporting_facts and not contradicting_facts and not knowledge_gaps:
                knowledge_gaps.append(f"No direct evidence found for hypothesis: {causal_hypothesis}")
                is_proven = False

        return {
            'hypothesis': causal_hypothesis,
            'is_proven': bool(is_proven),
            'supporting_facts': supporting_facts,
            'contradicting_facts': contradicting_facts,
            'knowledge_gaps': knowledge_gaps
        }

    def generate_proof(self, hypothesis: str, query_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a lightweight proof summary for the hypothesis.

        The proof includes a confidence score derived from matching evidence
        in `query_results` (e.g., similarity scores or explicit do-calculus scores).
        """
        best_score = 0.0
        supporting = []
        contradicting = []
        for r in (query_results or []):
            sim = float(r.get('similarity', r.get('score', 0.0) or 0.0))
            if sim > 0.7:
                supporting.append(r)
            elif sim < 0.3:
                contradicting.append(r)
            if sim > best_score:
                best_score = sim

        proof = {
            'hypothesis': hypothesis,
            'is_proven': best_score > 0.85,
            'confidence': round(best_score, 4),
            'supporting_count': len(supporting),
            'contradicting_count': len(contradicting),
            'supporting': supporting[:5]
        }
        return proof
