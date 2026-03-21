import numpy as np
import networkx as nx

class RFSimulator:
    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
            
    def apply_rf_model(self, graph: nx.Graph):
        edges_to_remove = []
        
        for u, v, data in graph.edges(data=True):
            dist = data.get('distance', 0)
            
            if dist > 50:
                edges_to_remove.append((u, v))
                continue
            elif dist < 15:
                bitrate = 54
            elif dist < 30:
                bitrate = 24
            else:
                bitrate = 6
                
            base_fer = (dist / 50.0) * 0.98 + 0.01
            noise = np.random.normal(0, 0.05)
            fer = float(np.clip(base_fer + noise, 0.01, 0.99))
            
            graph[u][v]['bitrate'] = bitrate
            graph[u][v]['e_f'] = fer
            
        graph.remove_edges_from(edges_to_remove)
        return graph
