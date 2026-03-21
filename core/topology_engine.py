import networkx as nx
import numpy as np
import math

class TopologyEngine:
    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        self.graph = nx.Graph()

    def calculate_euclidean_distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def generate_random_topology(self, num_nodes, max_x=100, max_y=100):
        self.graph.clear()
        positions = {}
        for i in range(num_nodes):
            x = np.random.uniform(0, max_x)
            y = np.random.uniform(0, max_y)
            positions[i] = (x, y)
            self.graph.add_node(i, pos=(x, y))

        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                dist = self.calculate_euclidean_distance(positions[i], positions[j])
                self.graph.add_edge(i, j, distance=dist)
        
        return self.graph
