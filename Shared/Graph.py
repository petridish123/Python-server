
# this program will take in a np matrix dxd and spit out a single graph that shows the strength of bonds as observed by the player k


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



def plot_directional_graph(matrix, labels=None, threshold=0.1, t=0,k=0):
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
    # plt.show()
    plt.clf()
    plt.imshow(matrix)
    plt.savefig(f"figures/figure{t}_{k}.png")

# matrix = np.array(
# [[ 0.,   -0.81,  0.99],
#  [-0.99 , 0.   ,-0.99],
#  [ 0.99 , 0.99 , 0.  ]])

# plot_directional_graph(matrix)

# plt.imshow(matrix)
# plt.show()


"""
This new function will use imshow
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_matrix_with_labels(matrix, labels=None, cmap='bwr_r', value_format='{:.2f}', t=0,k=0):
    D = matrix.shape[0]
    if labels is None:
        labels = [f"N{i}" if i!=k else f"N{i} (you)" for i in range(D)]

    fig, ax = plt.subplots(figsize=(6, 6))

    # Fixed color range so 0 is always visible
    im = ax.imshow(matrix, cmap=cmap, aspect='equal', vmin=-2, vmax=2)

    # Add colorbar with fixed ticks including 0
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Connection Strength", rotation=270, labelpad=15)
    cbar.set_ticks(np.linspace(-2, 2, 5))

    # Set ticks and labels
    ax.set_xticks(np.arange(D))
    ax.set_yticks(np.arange(D))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    # Move x-axis labels to top
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    # Rotate x labels for readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")

    # Add value labels
    for i in range(D):
        for j in range(D):
            val = matrix[i, j]
            ax.text(j, i, value_format.format(val),
                    ha="center", va="center",
                    color="black" if abs(val) < 1.4 else "white",
                    fontsize=10, fontweight='bold')

    ax.set_title("Directed Strength Matrix", pad=20)
    plt.tight_layout()
    plt.savefig(f"figures/figure{t}_{k}")




# Example usage
# D = 5
# np.random.seed(42)
# matrix = np.random.uniform(-1, 1, (D, D))
# plot_matrix_with_labels(matrix, labels=[f"Node {i+1}" for i in range(3)])
