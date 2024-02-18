# Copyright (c) 2024 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Provides methods for network analysis."""

import networkx as nx
import pandas as pd
import operator
import pathlib
import matplotlib.pyplot as plt


def degree_centrality(G, weight=None):
    """Compute degree centrality for the nodes."""
    centrality = list(nx.degree_centrality(G).values())
    centrality = {n: d for n, d in zip(G.nodes, centrality)}
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def eigenvector_centrality(G, weight=None):
    """Compute eigenvector centrality for the nodes."""
    centrality = list(nx.eigenvector_centrality(G, weight=weight).values())
    centrality = {n: d for n, d in zip(G.nodes, centrality)}
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def betweenness_centrality(G, weight=None):
    """Compute betweenness centrality for the nodes."""
    centrality = list(nx.betweenness_centrality(G, weight=weight).values())
    centrality = {n: d for n, d in zip(G.nodes, centrality)}
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def edge_betweenness_centrality(G, weight=None):
    """Compute betweenness centrality for the edges."""
    centrality = list(nx.edge_betweenness_centrality(G, weight=weight).values())
    centrality = {n: d for n, d in zip(G.edges, centrality)}
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def closeness_centrality(G, weight=None):
    """Compute closeness centrality for the nodes."""
    centrality = list(nx.closeness_centrality(G, distance=weight).values())
    centrality = {n: d for n, d in zip(G.nodes, centrality)}
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def pagerank(G, weight=None):
    """Compute PageRank for the nodes."""
    rank = list(nx.pagerank(G, weight=weight).values())
    rank = {n: d for n, d in zip(G.nodes, rank)}
    rank = dict(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))
    return rank


def articulation_points(G):
    """Find the articulation points of the network."""
    if nx.is_directed(G):
        return list(nx.articulation_points(G.to_undirected()))
    else:
        return list(nx.articulation_points(G))


def largest_connected_component(G):
    """Return size of largest connected component of the network."""
    return len(max(nx.connected_components(G), key=len))


def largest_connected_component_subgraph(G):
    """Return largest connected component as a subgraph."""
    lcc = max(nx.connected_components(G), key=len)
    return G.subgraph(lcc).copy()


def second_largest_connected_component(G):
    """Return size of second-largest connected component of the network."""
    slcc = [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    if len(slcc) > 1:
        return slcc[1]
    else:
        return 0


def global_efficiency(G, weight=None):
    """Return global efficiency of the network.

    Reference:
        - Latora, V., and Marchiori, M. (2001). Efficient behavior of
          small-world networks. Physical Review Letters 87.
        - Latora, V., and Marchiori, M. (2003). Economic small-world behavior
          in weighted networks. Eur Phys J B 32, 249-263.
        - Bellingeri, M., Bevacqua, D., Scotognella, F. et al. A comparative
          analysis of link removal strategies in real complex weighted networks.
          Sci Rep 10, 3911 (2020). https://doi.org/10.1038/s41598-020-60298-7
    """
    n = G.number_of_nodes()
    if n < 2:
        eff = 0
    else:
        inv_d = []
        for node in G:
            if weight is None:
                dij = nx.single_source_shortest_path_length(G, node)
            else:
                dij = nx.single_source_dijkstra_path_length(G, node, weight=weight)
            inv_dij = [1 / d for d in dij.values() if d != 0]
            inv_d.extend(inv_dij)
        eff = sum(inv_d) / (n * (n - 1))
    return eff


class NetworkAnalysis:
    """Class for doing network analysis on graphs."""
    def __init__(self, G=None):
        self.graph = None
        if G:
            if (
                isinstance(G, nx.Graph)
                or isinstance(G, nx.DiGraph)
                or isinstance(G, nx.MultiGraph)
            ):
                self.graph = G

    def read_edgelist(
        self,
        filename,
        comments="#",
        delimiter=None,
        create_using=nx.Graph,
        nodetype=None,
        data=True,
        encoding="utf-8",
    ):
        """Read a graph from a list of edges."""
        self.graph = nx.read_edgelist(
            filename,
            comments=comments,
            delimiter=delimiter,
            create_using=create_using,
            nodetype=nodetype,
            data=data,
            encoding=encoding,
        )

    def read_adjacency(self, filename, index_col=0, create_using=nx.Graph):
        """Load network from CSV file with interdependency matrix."""
        if pathlib.Path(filename).suffix == ".csv":
            df = pd.read_csv(filename, index_col=index_col)
            # need to make sure dependency is interpreted as j --> i
            self.graph = nx.from_pandas_adjacency(
                df.transpose(), create_using=create_using
            )
        else:
            self.graph = None

    def degree_centrality(self):
        return degree_centrality(self.graph)

    def eigenvector_centrality(self, weight=None):
        return eigenvector_centrality(self.graph, weight=weight)

    def betweenness_centrality(self, weight=None):
        return betweenness_centrality(self.graph, weight=weight)

    def edge_betweenness_centrality(self, weight=None):
        return edge_betweenness_centrality(self.graph, weight=weight)

    def closeness_centrality(self, distance=None):
        return closeness_centrality(self.graph, weight=distance)

    def pagerank(self, weight=None):
        return pagerank(self.graph, weight=None)

    def articulation_points(self):
        return articulation_points(self.graph)

    def largest_connected_component(self):
        return largest_connected_component(self.graph)

    def largest_connected_component_subgraph(self):
        return largest_connected_component_subgraph(self.graph)

    def second_largest_connected_component(self):
        return second_largest_connected_component(self.graph)

    def global_efficiency(self, weight=None):
        return global_efficiency(self.graph, weight=weight)

    def draw(
        self, layout=None, node_size=300, with_labels=True, figsize=(12, 12), dpi=300
    ):
        _, ax = plt.subplots(figsize=figsize, dpi=dpi)
        pos = layout(self.graph)
        nx.draw_networkx(
            self.graph, pos=pos, ax=ax, node_size=node_size, with_labels=with_labels
        )
