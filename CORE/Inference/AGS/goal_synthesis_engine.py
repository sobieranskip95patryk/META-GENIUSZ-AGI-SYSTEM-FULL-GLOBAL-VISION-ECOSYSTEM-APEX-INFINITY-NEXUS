"""CORE/Inference/AGS/goal_synthesis_engine.py
Goal synthesis and prioritization engine for AGS (Phase II, Step 4)
"""
from typing import Dict, Any, Optional
import time

try:
    from CORE.Memory.long_term_graph import LongTermGraphManager
except Exception:
    LongTermGraphManager = None

try:
    from CORE.Inference.logos_language_generator import LogosLanguageSynthesizer as LogosLanguageGenerator
except Exception:
    LogosLanguageGenerator = None


class GoalSynthesisEngine:
    """Synthesize and prioritize autonomous goals using causal analysis,
    optional LogosLanguageGenerator and LongTermGraphManager.
    """

    def __init__(self, ltm: Optional[LongTermGraphManager] = None, ll_generator: Optional[LogosLanguageGenerator] = None):
        self.ltm = ltm
        self.ll_generator = ll_generator

    def ags_synthesize_goal(self, causal_analysis_results: Dict[str, Any], current_state: Any) -> Dict[str, Any]:
        """Primary API: returns a dict with keys 'goal','priority','reason',
        'target_coherence_p' and 'target_autonomy_level'.
        """
        is_proven = bool(causal_analysis_results.get('is_proven', False))
        supporting = causal_analysis_results.get('supporting_facts', []) or []
        contradicting = causal_analysis_results.get('contradicting_facts', []) or []
        gaps = causal_analysis_results.get('knowledge_gaps', []) or []
        hypothesis = causal_analysis_results.get('hypothesis', causal_analysis_results.get('causal_hypothesis', 'unspecified'))

        proof_weight = 0.0
        if is_proven:
            proof_weight = 1.0 - (len(contradicting) * 0.2 + len(gaps) * 0.3)
            proof_weight = max(0.0, proof_weight)

        if not is_proven:
            goal_direction = "investigate knowledge gaps and resolve contradictions"
            reason = f"To address uncertainty for: '{hypothesis}'."
            if gaps:
                reason += f" Key gaps: {'; '.join(gaps)}."
            if contradicting:
                reason += f" Contradictions: {'; '.join(contradicting)}."
            autonomy_level = getattr(current_state, 'autonomy_level', 0.5) if current_state is not None else 0.5
            priority = autonomy_level * 0.5
            priority = min(1.0, max(0.05, priority))
            final_goal_text = f"Synthesize Goal: {goal_direction}"
        else:
            goal_formulation_input = {
                'causal_hypothesis': hypothesis,
                'proof_strength': proof_weight,
                'current_state': getattr(current_state, '__dict__', current_state) if current_state is not None else {},
                'supporting_facts': supporting
            }

            synthesized_goal_text = None
            try:
                if self.ll_generator and hasattr(self.ll_generator, 'synthesize_goal'):
                    synthesized_goal_text = self.ll_generator.synthesize_goal(goal_formulation_input=goal_formulation_input)
            except Exception:
                synthesized_goal_text = None

            if not synthesized_goal_text:
                synthesized_goal_text = f"Increase coherence by mitigating {hypothesis}" if hypothesis else "Improve system coherence"

            autonomy_level = getattr(current_state, 'autonomy_level', 0.5) if current_state is not None else 0.5
            priority = (autonomy_level * 0.7 + proof_weight * 0.3)
            priority = min(1.0, max(0.1, priority))

            goal_direction = synthesized_goal_text
            reason = f"Derived from causal proof (weight: {proof_weight:.2f}) and current system state, aiming to {synthesized_goal_text}."
            final_goal_text = f"Synthesize Goal: {goal_direction}"

        # Historical enrichment
        historical_insights = []
        try:
            if self.ltm and hasattr(self.ltm, 'semantic_search'):
                hist = self.ltm.semantic_search(final_goal_text, k=2) or []
                for h in hist:
                    if isinstance(h, dict):
                        val = h.get('content') or h.get('metadata', {}).get('content')
                    else:
                        val = str(h)
                    if val:
                        historical_insights.append(val)
        except Exception:
            historical_insights = []

        if historical_insights:
            reason += f" (Historical insights: {'; '.join(historical_insights)})"

        result = {
            'goal': final_goal_text,
            'priority': float(round(priority, 4)),
            'reason': reason,
            'target_coherence_p': float(round((getattr(current_state, 'coherence_p', 0.5) + (1 - getattr(current_state, 'coherence_p', 0.5)) * 0.1), 4)) if current_state is not None else 0.6,
            'target_autonomy_level': float(round((getattr(current_state, 'autonomy_level', 0.5) + (1 - getattr(current_state, 'autonomy_level', 0.5)) * 0.05), 4)) if current_state is not None else 0.525,
            'timestamp': time.time()
        }

        return result

    # Compatibility alias
    def synthesize(self, causal_proof: Dict[str, Any], current_state: Any) -> Dict[str, Any]:
        return self.ags_synthesize_goal(causal_proof, current_state)
