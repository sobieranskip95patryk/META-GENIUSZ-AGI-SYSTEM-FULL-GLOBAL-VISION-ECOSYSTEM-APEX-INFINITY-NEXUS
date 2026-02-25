"""
Pamięć długotrwała (Long Term Graph).
Dynamiczny graf relacyjny reprezentujący wiedzę o świecie (Uniwersalna Symbolika).
Implementuje Hybrydową Persystencję: Struktura (Graph) + Treść (Vector) -> .GOK Snapshot.
"""

import networkx as nx
import pickle
import json
import os
import time

GOK_FILE_EXTENSION = ".gok"
DEFAULT_STORAGE_PATH = "CORE/02_Memory/storage"

class LongTermGraphManager:
    def __init__(self, storage_path=DEFAULT_STORAGE_PATH):
        self.graph = nx.MultiDiGraph() # Multi-Directed Graph dla złożonych relacji
        self.vector_store = {} # Placeholder dla ChromaDB/FAISS (NodeID -> Vector)
        self.storage_path = storage_path
        
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def add_concept(self, node_id, attributes=None, embedding=None):
        """Dodaje węzeł do grafu i jego embedding do pamięci wektorowej."""
        if attributes is None:
            attributes = {}
        
        attributes['created_at'] = time.time()
        self.graph.add_node(node_id, **attributes)
        
        if embedding is not None:
            self.vector_store[node_id] = embedding

    def add_relation(self, source_id, target_id, relation_type, weight=1.0):
        """Dodaje krawędź (relację) między pojęciami."""
        self.graph.add_edge(source_id, target_id, type=relation_type, weight=weight)

    def add_fact(self, subject, obj, relation):
        """Wrapper dla prostego dodawania faktów (Testy/Dedukcja)."""
        if not self.graph.has_node(subject):
            self.graph.add_node(subject, type='Entity')
        if not self.graph.has_node(obj):
            self.graph.add_node(obj, type='Entity')
        self.add_relation(subject, obj, relation)


    def fetch_neighborhood_for_inference(self, node_id, depth=1):
        """
        Pobiera podgraf sąsiedztwa dla DualTruthEngine.
        Zwraca strukturę gotową do konwersji na edge_index (Tensor).
        """
        if node_id not in self.graph:
            return None
            
        # Pobranie sąsiadów do zadanej głębokości (ego graph)
        subgraph = nx.ego_graph(self.graph, node_id, radius=depth)
        return subgraph

    def add_triples(self, triples, source_id):
        """
        Dodaje trójki (fakty) do grafu wiedzy i tworzy relacje.
        To jest kluczowa funkcja dla wzrostu Complexity_G.
        """
        # Utworzenie węzłów kotwiczących (Source/Manifest)
        if not self.graph.has_node(source_id):
            self.graph.add_node(source_id, type='Manifest', coherence=1.0)
            
        for subject, relation, obj in triples:
            subj_node = f"Entity:{subject}"
            obj_node = f"Entity:{obj}"
            
            # Dodaj węzły, jeśli nie istnieją
            if not self.graph.has_node(subj_node):
                self.graph.add_node(subj_node, type='Entity', coherence=1.0)
                
            if not self.graph.has_node(obj_node):
                self.graph.add_node(obj_node, type='Entity', coherence=1.0)
                
            # Dodaj Krawędź Faktu (GCN Input)
            self.graph.add_edge(subj_node, obj_node, relation=relation)
            
            # Dodaj Krawędź do Manifestu (Księgowość Koherencji)
            # Każdy fakt jest powiązany ze swoim źródłem (source_id)
            self.graph.add_edge(source_id, subj_node, relation='documented_fact')
        
        # Zwiększ licznik Complexity_G w runtime (jeśli dotyczy)
        # Symulacja: Domyślne cechy węzłów zostaną wypełnione przez wektory w następnym kroku
        print(f"LTM: Dodano {len(triples)} nowych faktów do grafu. Aktualne węzły: {len(self.graph.nodes)}")


    def save_gok(self, filename="snapshot_latest"):
        """
        Tworzy migawkę .GOK (Genesis Operational Knowledge).
        Serializuje strukturę grafu i wektory do jednego binarnego pliku.
        """
        filepath = os.path.join(self.storage_path, filename + GOK_FILE_EXTENSION)
        
        payload = {
            'meta': {'timestamp': time.time(), 'nodes_count': self.graph.number_of_nodes()},
            'graph_data': nx.node_link_data(self.graph), # Serializacja NetworkX
            'vector_data': self.vector_store
        }
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(payload, f)
            print(f"[MEMORY] Saved .GOK snapshot: {filepath}")
            return True
        except Exception as e:
            print(f"[MEMORY] Error saving .GOK: {e}")
            return False

    def load_gok(self, filename="snapshot_latest"):
        """Ładuje stan grafu z pliku .GOK."""
        filepath = os.path.join(self.storage_path, filename + GOK_FILE_EXTENSION)
        
        if not os.path.exists(filepath):
            print(f"[MEMORY] Snapshot not found: {filepath}")
            return False
            
        try:
            with open(filepath, 'rb') as f:
                payload = pickle.load(f)
                
            self.graph = nx.node_link_graph(payload['graph_data'])
            self.vector_store = payload['vector_data']
            print(f"[MEMORY] Loaded .GOK snapshot. Nodes: {self.graph.number_of_nodes()}")
            return True
        except Exception as e:
            print(f"[MEMORY] Error loading .GOK: {e}")
            return False

    def load_axioms(self, axioms_path):
        """Wstrzykuje aksjomaty z pliku JSON do grafu jako węzły kotwiczące."""
        try:
            with open(axioms_path, 'r') as f:
                data = json.load(f)
                
            axioms = data.get("AXIOMS", {})
            count = 0
            for key, val in axioms.items():
                node_id = f"AXIOM_{key}"
                self.add_concept(node_id, attributes=val)
                # Twarde powiązanie z Węzłem Centralnym (gdyby istniał)
                # self.add_relation(node_id, "ROOT_CONCEPT", "DEFINES")
                count += 1
            
            print(f"[MEMORY] Injected {count} axioms from {axioms_path}")
            return True
        except Exception as e:
            print(f"[MEMORY] Failed to load axioms: {e}")
            return False

    # --- Semantic search + simple caching (T2 Phase IV profiling helper) ---
    def _simple_embed(self, text):
        """Placeholder embedder: deterministic lightweight embedding for tests.
        Replace with real encoder (OpenAI/embedding model) in production.
        """
        vec = [float((ord(c) % 97) / 97.0) for c in text[:128]]
        L = 32
        if len(vec) < L:
            vec = vec + [0.0] * (L - len(vec))
        else:
            vec = vec[:L]
        return vec

    def _cosine_sim(self, a, b):
        """Compute cosine similarity for two equal-length vectors."""
        sa = sum(x * x for x in a) ** 0.5
        sb = sum(x * x for x in b) ** 0.5
        if sa == 0 or sb == 0:
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        return dot / (sa * sb)

    def semantic_search(self, query_text, top_k=5, use_cache=True, cache_ttl=300):
        """Return top_k node_ids most semantically similar to `query_text`.

        Lightweight implementation for testing. In production, delegate to
        a proper embedder and vector DB. This includes an in-memory cache
        with TTL to speed repeated queries during profiling.
        """
        if not hasattr(self, '_semantic_cache'):
            self._semantic_cache = {}

        cache_key = (query_text, top_k)
        now = time.time()
        if use_cache:
            entry = self._semantic_cache.get(cache_key)
            if entry is not None:
                ts, value = entry
                if now - ts < cache_ttl:
                    return value

        qvec = self._simple_embed(query_text)

        scores = []
        for node_id, emb in self.vector_store.items():
            try:
                sim = self._cosine_sim(qvec, emb)
            except Exception:
                sim = 0.0
            scores.append((sim, node_id))

        scores.sort(reverse=True)
        result = [nid for _, nid in scores[:top_k]]

        if use_cache:
            self._semantic_cache[cache_key] = (now, result)

        return result


# Alias dla kompatybilności
LongTermGraph = LongTermGraphManager
