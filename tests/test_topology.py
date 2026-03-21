import pytest
import networkx as nx
from core.topology_engine import TopologyEngine

def test_initialization():
    engine = TopologyEngine()
    assert isinstance(engine.graph, nx.Graph)
    assert len(engine.graph.nodes) == 0

def test_euclidean_distance():
    engine = TopologyEngine()
    pos1 = (0, 0)
    pos2 = (3, 4)
    assert engine.calculate_euclidean_distance(pos1, pos2) == 5.0

def test_deterministic_generation():
    engine1 = TopologyEngine(seed=42)
    graph1 = engine1.generate_random_topology(5, 100, 100)
    
    engine2 = TopologyEngine(seed=42)
    graph2 = engine2.generate_random_topology(5, 100, 100)
    
    for i in range(5):
        assert graph1.nodes[i]['pos'] == graph2.nodes[i]['pos']
    
    assert list(graph1.edges(data=True)) == list(graph2.edges(data=True))
