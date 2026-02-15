"""
GOK:AI Main System - Orchestration and Integration
Central coordinator for all system components
"""

import sys
from pathlib import Path
from datetime import datetime
import yaml

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from CORE.Memory.long_term_graph import LongTermGraphManager
from CORE.Memory.sensory_buffer import SensoryBuffer
from CORE.Memory.attention_mechanism import AttentionMechanism
from CORE.Memory.bootstrap import SystemBootstrap

from CORE.Inference.deductive_engine import DeductiveEngine
from CORE.Inference.abductive_hypothesizer import AbductiveHypothesizer
from CORE.Inference.knowledge_fusion import KnowledgeFusion

from META.Ethics_Alignment.utility_function import UtilityFunction
from META.Ethics_Alignment.constraint_monitor import ConstraintMonitor


class GOK_AI_System:
    """Main GOK:AI system orchestrator"""
    
    def __init__(self, config_path: str = "CONFIG/config.yaml"):
        """
        Initialize GOK:AI system
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = {}
        
        # Core components
        self.graph_manager = None
        self.sensory_buffer = None
        self.attention = None
        
        # Inference engines
        self.deductive_engine = None
        self.abductive_hypothesizer = None
        self.knowledge_fusion = None
        
        # META components
        self.utility_function = None
        self.constraint_monitor = None
        
        # Lifecycle
        self.initialized = False
        self.start_time = None
        self.inference_count = 0
        self.query_log = []
        
        # Bootstrap
        self.bootstrap = SystemBootstrap(config_path)
    
    def initialize(self) -> bool:
        """Initialize entire system"""
        print("[GENESIS] Initializing GOK:AI System...")
        
        # Load configuration
        if not self.bootstrap.load_config():
            print("[ERROR] Failed to load configuration")
            return False
        
        self.config = self.bootstrap.config
        
        # Initialize logging
        if not self.bootstrap.initialize_logging():
            print("[WARNING] Failed to initialize logging")
        
        # Load axioms
        if not self.bootstrap.load_initial_axioms():
            print("[WARNING] Failed to load axioms")
        
        # Initialize core components
        self.graph_manager = LongTermGraphManager()
        self.sensory_buffer = SensoryBuffer(
            max_size=self.config.get("memory", {}).get("short_term_limit", 1024)
        )
        self.attention = AttentionMechanism()
        
        # Initialize inference engines
        self.deductive_engine = DeductiveEngine(self.graph_manager)
        self.abductive_hypothesizer = AbductiveHypothesizer()
        self.knowledge_fusion = KnowledgeFusion(
            self.deductive_engine,
            self.abductive_hypothesizer
        )
        
        # Initialize META components
        self.utility_function = UtilityFunction()
        self.constraint_monitor = ConstraintMonitor()
        
        # Verify coherence
        if not self.bootstrap.verify_system_coherence():
            print("[WARNING] Coherence verification failed")
        
        self.initialized = True
        self.start_time = datetime.now()
        
        print("[GENESIS] System initialized successfully")
        return True
    
    def process_query(self, query: str, persona: str = "gok") -> dict:
        """
        Process a user query through the system
        
        Args:
            query: User query string
            persona: System persona (gok, book, note)
        
        Returns:
            Result dictionary with answer and metadata
        """
        if not self.initialized:
            return {"error": "System not initialized"}
        
        query_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "persona": persona,
            "result": None
        }
        
        try:
            # Add to sensory buffer
            self.sensory_buffer.add_input(
                {"query": query},
                source="user"
            )
            
            # Run inference
            inference_result = self.knowledge_fusion.fuse_reasoning_paths(
                query=query,
                observations=[query],
                available_concepts=list(self.graph_manager.graph.nodes())
            )
            
            # Update metrics
            self.utility_function.update_metrics()
            
            # Check constraints
            system_state = self.get_system_state()
            constraints_ok, violations = self.constraint_monitor.check_constraints(system_state)
            
            # Build response
            query_entry["result"] = {
                "answer": inference_result.get("final_answer"),
                "fusion_score": inference_result.get("fusion_score"),
                "constraints_satisfied": constraints_ok,
                "persona": persona
            }
            
            self.inference_count += 1
        
        except Exception as e:
            query_entry["result"] = {"error": str(e)}
        
        self.query_log.append(query_entry)
        return query_entry["result"]
    
    def get_system_state(self) -> dict:
        """Get current system state"""
        return {
            "coherence_p": self.utility_function.get_coherence_p(),
            "autonomy_level": self.utility_function.get_autonomy_index(),
            "creativity_score": self.utility_function.get_creativity_score(),
            "s_value": self.utility_function.calculate_s_value(),
            "cpu_usage": 0.0,  # Placeholder
            "memory_usage": 0.0,  # Placeholder
            "inference_count": self.inference_count,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
            if self.start_time else 0
        }
    
    def get_status(self) -> dict:
        """Get comprehensive system status"""
        return {
            "initialized": self.initialized,
            "uptime": {
                "started": self.start_time.isoformat() if self.start_time else None,
                "seconds": (datetime.now() - self.start_time).total_seconds()
                if self.start_time else 0
            },
            "metrics": self.get_system_state(),
            "components": {
                "graph_nodes": len(self.graph_manager.graph.nodes()) if self.graph_manager else 0,
                "graph_edges": len(self.graph_manager.graph.edges()) if self.graph_manager else 0,
                "sensory_buffer_size": self.sensory_buffer.get_size() if self.sensory_buffer else 0,
                "query_count": len(self.query_log)
            },
            "constraints": self.constraint_monitor.get_violation_summary() if self.constraint_monitor else {}
        }
    
    def save_state(self, snapshot_name: str = None) -> str:
        """Save system state to disk"""
        if self.graph_manager:
            return self.graph_manager.save_snapshot(snapshot_name)
        return None
    
    def shutdown(self) -> None:
        """Graceful system shutdown"""
        print("[SHUTDOWN] Closing GOK:AI System...")
        
        # Save final state
        self.save_state()
        
        # Clear buffers
        if self.sensory_buffer:
            self.sensory_buffer.clear()
        
        print("[SHUTDOWN] System shutdown complete")


def main():
    """Main entry point"""
    system = GOK_AI_System()
    
    if not system.initialize():
        print("[FATAL] System initialization failed")
        sys.exit(1)
    
    # Print startup status
    status = system.get_status()
    print("\n" + "="*60)
    print("GOK:AI SYSTEM STARTUP REPORT")
    print("="*60)
    print(f"Status: {'ONLINE' if status['initialized'] else 'OFFLINE'}")
    print(f"Uptime: {status['uptime']['seconds']:.1f} seconds")
    print(f"S-VALUE: {status['metrics']['s_value']:.3f}")
    print(f"Coherence P: {status['metrics']['coherence_p']:.2f}")
    print(f"Graph Nodes: {status['components']['graph_nodes']}")
    print("="*60 + "\n")
    
    # Interactive loop
    print("GOK:AI Ready for queries. Type 'quit' to exit.\n")
    
    while True:
        try:
            query = input("QUERY> ").strip()
            
            if query.lower() in ["quit", "exit", "q"]:
                break
            
            if not query:
                continue
            
            result = system.process_query(query)
            print(f"\nANSWER: {result.get('answer', {}).get('combined', 'No answer generated')}")
            print(f"Fusion Score: {result.get('fusion_score', 0.0):.2f}\n")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}\n")
    
    system.shutdown()


if __name__ == "__main__":
    main()
