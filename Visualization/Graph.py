# import matplotlib.pyplot as plt

# this program will take in a np matrix dxd and spit out a single graph that shows the strength of bonds as observed by the player k


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

M = np.array([
    [0, 2, 3, 0],
    [7, 0, 0, 4],
    [0, 5, 0, 2],
    [3, 0, 1, 0]
])

M = np.array([
    [0, 2, 3],
    [7, 0, 0],
    [0, 5, 0],
    
])

def plot_directional_graph(matrix, labels=None, threshold=0, title="Directional Strength Graph"):
    """
    Visualize a square matrix as a directed weighted graph.
    
    Parameters:
    -----------
    matrix : array-like (D x D)
        Square matrix where element [i, j] represents strength from node i to node j.
    labels : list of str, optional
        Custom labels for nodes. Defaults to numeric indices starting at 1.
    threshold : float, optional
        Only show edges with weight > threshold.
    title : str, optional
        Title for the plot.
    """
    # Convert to NumPy array
    M = np.array(matrix)
    if M.shape[0] != M.shape[1]:
        raise ValueError("Matrix must be square (DxD).")

    n = M.shape[0]
    if labels is None:
        labels = [str(i+1) for i in range(n)]
    elif len(labels) != n:
        raise ValueError("Length of labels must match matrix size.")

    # Build directed graph
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if M[i, j] > threshold:
                G.add_edge(labels[i], labels[j], weight=M[i, j])

    # Layout and drawing
    pos = nx.spring_layout(G, seed=42)
    edges = G.edges(data=True)
    weights = [d['weight'] for _, _, d in edges]

    nx.draw(
        G, pos, with_labels=True, node_size=800,
        node_color='skyblue', arrows=True,
        width=[max(w/np.max(weights)*3, 0.5) for w in weights],  # scale edge width
        edge_color='gray', font_size=10
    )

    # Edge labels (weights)
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in edges},
        font_color='darkred', font_size=8
    )

    plt.title(title)
    plt.axis('off')
    plt.show()

plot_directional_graph(M)
