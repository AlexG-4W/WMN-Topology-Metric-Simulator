import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

class NetworkVisualizer:
    def __init__(self):
        pass

    def draw_network(self, G, hop_path, alm_path, source_node, target_node):
        pos = nx.get_node_attributes(G, 'pos')
        
        plt.figure(figsize=(10, 8))
        
        # Base graph edges and nodes
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3)
        nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=300)
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        # Hop Count Path
        hop_edges = list(zip(hop_path, hop_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=hop_edges, edge_color='red', width=3, style='dashed')
        
        # ALM Path
        alm_edges = list(zip(alm_path, alm_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=alm_edges, edge_color='green', width=2)
        
        # Highlight Source and Target
        nx.draw_networkx_nodes(G, pos, nodelist=[source_node, target_node], node_color='blue', node_size=400)
        
        # Legend
        red_line = mlines.Line2D([], [], color='red', linewidth=3, linestyle='dashed', label='Hop Count Path')
        green_line = mlines.Line2D([], [], color='green', linewidth=2, label='ALM Path')
        plt.legend(handles=[red_line, green_line], loc='best')
        
        plt.title('WMN Topology: Hop Count vs ALM Routing')
        plt.axis('off')
        
        # Save and close
        plt.savefig('wmn_simulation_result.png', dpi=300, bbox_inches='tight')
        plt.close()
