
# this program will take in a np matrix dxd and spit out a single graph that shows the strength of bonds as observed by the player k


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_directional_graph(matrix, labels=None, threshold=0.0,t=1,k=1):
    """
    Plots a directed network graph from a D x D matrix.
    
    Args:
        matrix (np.ndarray): A square matrix of shape (D, D), where M[i, j]
                             is the strength from node i to node j.
        labels (list): Optional list of node labels (length D).
        threshold (float): Minimum absolute strength to display an edge.
    """
    D = matrix.shape[0]
    if labels is None:
        labels = [f"N{i}" for i in range(D)]
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes
    for i, label in enumerate(labels):
        G.add_node(i, label=label)
    
    # Add edges based on threshold
    for i in range(D):
        for j in range(D):
            if i != j and abs(matrix[i, j]) > threshold:
                G.add_edge(i, j, weight=matrix[i, j])
    
    # Position nodes using spring layout
    pos = nx.spring_layout(G, seed=42)
    
    # Extract weights for edge thickness
    weights = [abs(G[u][v]['weight']) for u, v in G.edges()]
    max_weight = max(weights) if weights else 1
    normalized_weights = [3 * (w / max_weight) for w in weights]
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
    
    # Draw edges with arrow style
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20,
                           width=normalized_weights, edge_color='gray')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, labels={i: label for i, label in enumerate(labels)},
                            font_size=12, font_weight='bold')
    
    # Add edge labels (optional)
    edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title("Directed Strength Network", fontsize=14)
    plt.axis('off')
    plt.show()
    plt.savefig(f"figures/figure{t}_{k}.png")

# # Example usage
# D = 5
# np.random.seed(0)
# matrix = np.random.randn(D, D)  # random strengths (can be positive or negative)
# plot_directed_strength_graph(matrix, labels=[f"Node {i+1}" for i in range(D)], threshold=0.2)

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def plot_directional_graph(matrix, labels=None, threshold=0.1, t=0,k=0):
    """
    Plots a directed network graph from a D x D matrix, showing edges i→j and j→i separately.
    
    Args:
        matrix (np.ndarray): Square matrix (D x D), where M[i,j] is strength from node i to node j.
        labels (list): Optional list of node labels.
        threshold (float): Minimum |strength| for an edge to be shown.
    """
    D = matrix.shape[0]
    if labels is None:
        labels = [f"N{i}" for i in range(D)]

    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes
    for i, label in enumerate(labels):
        print(f"i: {i} label: {label}")
        G.add_node(i, label=label)
    
    # Add edges (i→j)
    for i in range(D):
        for j in range(D):
            if i != j and abs(matrix[i, j]) > threshold:
                G.add_edge(i, j, weight=matrix[i, j])
    
    
    # Position nodes
    pos = nx.spring_layout(G, seed=42)
    
    # Edge attributes
    weights = np.array([abs(G[u][v]['weight']) for u, v in G.edges()])
    max_w = weights.max() if len(weights) > 0 else 1
    widths = 2 + 3 * (weights / max_w)
    print(G.edges())
    print(weights)
    # Edge colors based on sign
    colors = ['green' if G[u][v]['weight'] > 0 else 'red' for u, v in G.edges()]
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    
    nx.draw_networkx_labels(G, pos, labels={i: label for i, label in enumerate(labels)}, font_weight='bold')

    # Draw edges with curvature so both directions are visible
    for (u, v, w), width, color in zip(G.edges(data='weight'), widths, colors):
        rad = 0.2 if G.has_edge(v, u) else 0.0  # curve if reverse edge exists
        nx.draw_networkx_edges(
            G, pos,
            edgelist=[(u, v)],
            arrowstyle='-|>',
            arrowsize=20,
            width=width,
            edge_color=color,
            connectionstyle=f'arc3,rad={rad}'
        )
    

    edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges()}
    print(edge_labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=9)
    print(matrix)
    print(f"player {k}")
    plt.title("Directed Network Graph (i→j and j→i)", fontsize=14)
    plt.axis('off')
    plt.show()
    plt.savefig(f"figures/figure{t}_{k}.png")



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
    plt.show()

matrix = np.array(
[[ 0.,   -0.81,  0.99],
 [-0.99 , 0.   ,-0.99],
 [ 0.99 , 0.99 , 0.  ]])

plot_directional_graph(matrix)

# plt.imshow(matrix)
# plt.show()


"""
This new function will use imshow
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_matrix_with_labels(matrix, labels=None, cmap='bwr_r', value_format='{:.2f}'):
    """
    Visualize a D x D matrix using imshow with overlaid value labels and axis tick labels.

    Args:
        matrix (np.ndarray): Square matrix (D x D)
        labels (list): Optional list of labels for rows/columns
        cmap (str): Matplotlib colormap name
        value_format (str): Format string for cell text
    """
    D = matrix.shape[0]
    if labels is None:
        labels = [f"N{i}" for i in range(D)]

    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Show the matrix as a heatmap
    im = ax.imshow(matrix, cmap=cmap, aspect='equal')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Connection Strength", rotation=270, labelpad=15)
    
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

    # Loop over data to create text annotations
    for i in range(D):
        for j in range(D):
            val = matrix[i, j]
            ax.text(j, i, value_format.format(val),
                    ha="center", va="center",
                    color="black" if abs(val) < np.max(abs(matrix)) * 0.7 else "white",
                    fontsize=10, fontweight='bold')

    ax.set_title("Directed Strength Matrix", pad=20)
    plt.tight_layout()
    plt.show()


# Example usage
# D = 5
# np.random.seed(42)
# matrix = np.random.uniform(-1, 1, (D, D))
plot_matrix_with_labels(matrix, labels=[f"Node {i+1}" for i in range(3)])
