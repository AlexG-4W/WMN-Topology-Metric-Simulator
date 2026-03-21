import networkx as nx
import argparse
from core.topology_engine import TopologyEngine
from core.rf_simulator import RFSimulator
from core.routing_engine import RoutingEngine
from core.visualizer import NetworkVisualizer
import random

def main():
    parser = argparse.ArgumentParser(description="WMN Topology & Metric Simulator")
    parser.add_argument("--nodes", type=int, default=30, help="Number of nodes in the mesh network")
    parser.add_argument("--width", type=float, default=100.0, help="Width of the simulation area in meters")
    parser.add_argument("--height", type=float, default=100.0, help="Height of the simulation area in meters")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible topologies")
    args = parser.parse_args()

    # 1. Topology Generation
    engine = TopologyEngine(seed=args.seed)
    G = engine.generate_random_topology(num_nodes=args.nodes, max_x=args.width, max_y=args.height)
    
    # 2. RF Simulation
    rf = RFSimulator(seed=args.seed)
    G = rf.apply_rf_model(G)
    
    # 3. Routing Engine
    re = RoutingEngine(G)
    re.calculate_alm_weights()
    
    source_node = 0
    target_node = args.nodes - 1
    
    import sys
    if not nx.has_path(G, source_node, target_node):
        print(f"No path exists between node {source_node} and {target_node}. Try a different seed or higher density.")
        sys.exit(0)
                    
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
