"""
MTaQuest — Hybrid Dialog Platform for GOK:AI

A sophisticated platform enabling real-time dialog between Architect (human)
and GOK:AI (AGI system) with intent quantization and vector synchronization.

Components:
-----------
- HybridDialogProtocol: Message standardization between Architect and GOK:AI
- IntentQuantizationEngine: Transform intents (I) + Knowledge (K) → Growth Vector (W)
- VectorSynchronizationEngine: Maintain state alignment between systems

Axiom: I + K = W
       Intent + Knowledge = Growth Vector

Version: 7.0
Author: Patryk Sobierański (Architect)
License: MIT
"""

__version__ = "7.0"
__author__ = "Patryk Sobierański"
__license__ = "MIT"

# Import core components
try:
    from .hybrid_dialog_protocol import (
        HybridDialogProtocol,
        IntentMessage,
        ResponseMessage,
        HybridDialogProtocol
    )
except ImportError as e:
    print(f"Warning: Could not import HybridDialogProtocol: {e}")

try:
    from .intent_quantization import (
        IntentQuantizationEngine,
        IntentVector,
        KnowledgeVector,
        GrowthVector,
        QuantizationPhase
    )
except ImportError as e:
    print(f"Warning: Could not import IntentQuantizationEngine: {e}")

try:
    from .vector_synchronization import (
        VectorSynchronizationEngine,
        VectorSnapshot,
        DivergenceMetric,
        ReconciliationStrategy,
        SyncPhase
    )
except ImportError as e:
    print(f"Warning: Could not import VectorSynchronizationEngine: {e}")

__all__ = [
    # Main components
    'HybridDialogProtocol',
    'IntentQuantizationEngine',
    'VectorSynchronizationEngine',
    
    # Data structures
    'IntentMessage',
    'ResponseMessage',
    'IntentVector',
    'KnowledgeVector',
    'GrowthVector',
    'VectorSnapshot',
    'DivergenceMetric',
    'ReconciliationStrategy',
    
    # Enums
    'QuantizationPhase',
    'SyncPhase',
]


def initialize_mtaquest(config=None):
    """
    Initialize MTaQuest platform with optional configuration
    
    Args:
        config (dict, optional): Configuration dictionary
            - embedding_dim: Dimension of embeddings (default: 768)
            - alignment_threshold: Threshold for alignment (default: 0.95)
            - sync_frequency: Sync check frequency in seconds (default: 0.5)
    
    Returns:
        dict: Initialized components
    
    Example:
        >>> components = initialize_mtaquest({
        ...     'embedding_dim': 768,
        ...     'alignment_threshold': 0.95
        ... })
        >>> hdp = components['hdp']
        >>> iqe = components['iqe']
        >>> vse = components['vse']
    """
    if config is None:
        config = {}
    
    components = {
        'hdp': HybridDialogProtocol(),
        'iqe': IntentQuantizationEngine(
            embedding_dim=config.get('embedding_dim', 768),
            knowledge_graph=config.get('knowledge_graph', None)
        ),
        'vse': VectorSynchronizationEngine(
            alignment_threshold=config.get('alignment_threshold', 0.95),
            sync_frequency=config.get('sync_frequency', 0.5)
        )
    }
    
    return components


# ==================== VERSION INFO ====================

class MTaQuestInfo:
    """MTaQuest platform information"""
    
    PROTOCOL_VERSION = "7.0"
    ASQK_O_ALPHA = 7.77  # Calibrated constant
    ALIGNMENT_THRESHOLD = 0.95
    EMBEDDING_DIM = 768
    
    @staticmethod
    def info():
        """Print MTaQuest information"""
        print("=" * 50)
        print("MTaQuest — Hybrid Dialog Platform")
        print("=" * 50)
        print(f"Version: {__version__}")
        print(f"Protocol: {MTaQuestInfo.PROTOCOL_VERSION}")
        print(f"ASQK-O Alpha: {MTaQuestInfo.ASQK_O_ALPHA}")
        print(f"Alignment Threshold: {MTaQuestInfo.ALIGNMENT_THRESHOLD}")
        print(f"Embedding Dimension: {MTaQuestInfo.EMBEDDING_DIM}")
        print("=" * 50)
        print("Components:")
        print("  ✓ HybridDialogProtocol (HDP)")
        print("  ✓ IntentQuantizationEngine (IQE)")
        print("  ✓ VectorSynchronizationEngine (VSE)")
        print("=" * 50)


# Display info on import
if __name__ != "__main__":
    # Uncomment for verbose startup
    # MTaQuestInfo.info()
    pass
