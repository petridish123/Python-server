import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def plot_directed_strength_graph(matrix, labels=None, threshold=0.0):
    """
    Plots a directed network graph from a D x D matrix, showing edges i→j and j→i separately,
    with curved arrows and visible labels for all weights (including negative ones).
    """
    D = matrix.shape[0]
    if labels is None:
        labels = [f"N{i}" for i in range(D)]

    # Create directed graph
    G = nx.DiGraph()

    for i, label in enumerate(labels):
        G.add_node(i, label=label)

    for i in range(D):
        for j in range(D):
            if i != j and abs(matrix[i, j]) > threshold:
                G.add_edge(i, j, weight=matrix[i, j])

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(8, 6))

    # Edge visual properties
    weights = np.array([abs(G[u][v]['weight']) for u, v in G.edges()])
    max_w = weights.max() if len(weights) > 0 else 1
    widths = 1.5 + 3 * (weights / max_w)
    colors = ['green' if G[u][v]['weight'] > 0 else 'red' for u, v in G.edges()]

    # Draw nodes and labels
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={i: label for i, label in enumerate(labels)},
                            font_weight='bold', ax=ax)

    # Draw directed curved edges
    for (u, v, w), width, color in zip(G.edges(data='weight'), widths, colors):
        # curve radius for bidirectional pairs
        rad = 0.25 if G.has_edge(v, u) else 0.0
        nx.draw_networkx_edges(
            G, pos,
            edgelist=[(u, v)],
            arrowstyle='-|>',
            arrowsize=20,
            width=width,
            edge_color=color,
            connectionstyle=f'arc3,rad={rad}',
            ax=ax
        )

        # Manually place label midway along the curve
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2  # midpoint of edge
        # offset the label slightly based on curvature
        dx = (y2 - y1) * rad
        dy = (x1 - x2) * rad
        ax.text(
            xm + dx * 0.5, ym + dy * 0.5,
            f"{w:.2f}",
            color=color,
            fontsize=9,
            fontweight='bold',
            ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1.5)
        )

    plt.title("Directed Network Graph with Bidirectional Strengths", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


# Example usage
D = 5
np.random.seed(1)
matrix = np.random.uniform(-1, 1, (D, D))  # directional strengths (positive & negative)
plot_directed_strength_graph(matrix, labels=[f"Node {i+1}" for i in range(D)], threshold=0.2)
