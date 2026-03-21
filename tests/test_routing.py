import pytest
import networkx as nx
from core.routing_engine import RoutingEngine

def test_routing_paths():
    graph = nx.Graph()
    graph.add_nodes_from(['A', 'B', 'C'])
    
    # Прямой линк A -> C: Дистанция 45м (битрейт 6 Мбит/с, высокий FER 0.8)
    graph.add_edge('A', 'C', distance=45, bitrate_mbps=6, fer=0.8)
    
    # Обходной путь A -> B -> C: Дистанции по 10м (битрейт 54 Мбит/с, низкий FER 0.05)
    graph.add_edge('A', 'B', distance=10, bitrate_mbps=54, fer=0.05)
    graph.add_edge('B', 'C', distance=10, bitrate_mbps=54, fer=0.05)
    
    engine = RoutingEngine(graph)
    engine.calculate_alm_weights()
    
    # Прямой путь по количеству хопов
    hop_path = engine.find_hop_count_path('A', 'C')
    assert hop_path == ['A', 'C']
    
    # Обходной путь по метрике ALM
    alm_path = engine.find_alm_path('A', 'C')
    assert alm_path == ['A', 'B', 'C']
