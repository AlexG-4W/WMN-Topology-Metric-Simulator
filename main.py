import networkx as nx
from core.topology_engine import TopologyEngine
from core.rf_simulator import RFSimulator
from core.routing_engine import RoutingEngine
from core.visualizer import NetworkVisualizer
import random

def main():
    # 1. Topology Generation
    te = TopologyEngine(seed=42)
    G = te.generate_random_topology(num_nodes=30, max_x=100, max_y=100)
    
    # 2. RF Simulation
    rf = RFSimulator(seed=42)
    G = rf.apply_rf_model(G)
    
    # 3. Routing Engine
    re = RoutingEngine(G)
    re.calculate_alm_weights()
    
    # Select connected source and target
    connected_components = list(nx.connected_components(G))
    largest_cc = max(connected_components, key=len)
    nodes = list(largest_cc)
    
    longest_path = 0
    source_node, target_node = nodes[0], nodes[1]
    
    # Find two nodes that are far apart
    for u in nodes:
        for v in nodes:
            if u != v and nx.has_path(G, u, v):
                path_len = nx.shortest_path_length(G, u, v)
                if path_len > longest_path:
                    longest_path = path_len
                    source_node = u
                    target_node = v
                    
    # Find paths
    hop_path = re.find_hop_count_path(source_node, target_node)
    alm_path = re.find_alm_path(source_node, target_node)
    
    # Calculate path metrics
    def calculate_path_alm(path, graph):
        total_alm = 0
        for u, v in zip(path, path[1:]):
            total_alm += graph[u][v]['alm_weight']
        return total_alm
        
    hop_alm_cost = calculate_path_alm(hop_path, G)
    alm_path_cost = calculate_path_alm(alm_path, G)
    
    print(f"Source Node: {source_node}, Target Node: {target_node}")
    print(f"--- Hop Count Path ---")
    print(f"Path: {hop_path}")
    print(f"Hop Count: {len(hop_path) - 1}")
    print(f"Total ALM Cost: {hop_alm_cost:.2f}")
    
    print(f"\n--- ALM Path ---")
    print(f"Path: {alm_path}")
    print(f"Hop Count: {len(alm_path) - 1}")
    print(f"Total ALM Cost: {alm_path_cost:.2f}")

    # 4. Visualization
    viz = NetworkVisualizer()
    viz.draw_network(G, hop_path, alm_path, source_node, target_node)

if __name__ == "__main__":
    main()
