import networkx as nx

class RoutingEngine:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def calculate_alm_weights(self):
        O = 400
        B_t = 8192
        for u, v, data in self.graph.edges(data=True):
            r = data.get('bitrate_mbps', data.get('bitrate', 1))
            e_f = data.get('fer', data.get('e_f', 0.5))
            
            # Prevent division by zero if FER is 1.0 or greater
            if e_f >= 1.0:
                e_f = 0.99
                
            c_a = (O + (B_t / (r * 10**6))) * (1 / (1 - e_f))
            self.graph[u][v]['alm_weight'] = c_a

    def find_hop_count_path(self, source, target):
        return nx.shortest_path(self.graph, source=source, target=target)

    def find_alm_path(self, source, target):
        return nx.shortest_path(self.graph, source=source, target=target, weight='alm_weight')
