# Copyright (c) 2024 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Provides methods for network analysis."""

import igraph as ig
import networkx as nx
import numpy as np
import pandas as pd
import operator
import pathlib
import matplotlib.pyplot as plt


def degree_centrality(G, weight=None):
    """Compute degree centrality for the nodes."""
    centrality = {G.vs[idx]: d / (G.vcount() - 1) for idx, d in enumerate(G.degree())}
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def eigenvector_centrality(G, weight=None):
    """Compute eigenvector centrality for the nodes."""
    centrality = {
        G.vs[idx]: d
        for idx, d in enumerate(
            G.eigenvector_centrality(directed=G.is_directed(), weights=weight, scale=False)
        )
    }
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def betweenness_centrality(G, weight=None):
    """Compute betweenness centrality for the nodes."""
    if G.is_directed():
        normalize = 1 / ((G.vcount() - 1) * (G.vcount() - 2))
    else:
        normalize = 2 / ((G.vcount() - 1) * (G.vcount() - 2))
    centrality = {
        G.vs[idx]: d * normalize
        for idx, d in enumerate(G.betweenness(directed=G.is_directed(), weights=weight))
    }
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def edge_betweenness_centrality(G, weight=None):
    """Compute betweenness centrality for the edges."""
    if G.is_directed():
        normalize = 1 / (G.vcount() * (G.vcount() - 1))
    else:
        normalize = 2 / (G.vcount() * (G.vcount() - 1))
    centrality = {
        G.es[idx]: d * normalize
        for idx, d in enumerate(
            G.edge_betweenness(directed=G.is_directed(), weights=weight)
        )
    }
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def closeness_centrality(G, weight=None):
    """Compute closeness centrality for the nodes."""
    centrality = {G.vs[idx]: d for idx, d in enumerate(G.closeness(weights=weight))}
    centrality = dict(
        sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    )
    return centrality


def pagerank(G, weight=None):
    """Compute PageRank for the nodes."""
    rank = {
        G.vs[idx]: d
        for idx, d in enumerate(G.pagerank(directed=G.is_directed(), weights=weight))
    }
    rank = dict(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))
    return rank


def articulation_points(G):
    """Find the articulation points of the network."""
    return G.articulation_points()


def largest_connected_component(G):
    """Return size of largest connected component of the network."""
    return G.connected_components().giant().vcount()


def largest_connected_component_subgraph(G):
    """Return largest connected component as a subgraph."""
    return G.connected_components().giant()


def second_largest_connected_component(G):
    """Return size of second-largest connected component of the network."""
    slcc = sorted(G.connected_components().sizes(), reverse=True)
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
    n = G.vcount()
    if n < 2:
        eff = 0
    else:
        inv_d = []
        for v in G.vs:
            dij = G.distances(v, weights=weight, mode="all")[0]
            inv_dij = [1 / d for d in dij if not (d == 0 or np.isinf(d))]
            inv_d.extend(inv_dij)
        eff = sum(inv_d) / (n * (n - 1))
    return eff


class NetworkAnalysis:
    """Class for doing network analysis on graphs."""
    def __init__(self, G=None):
        self.graph = None
        if G and isinstance(G, ig.Graph):
            self.graph = G

    def read(self, filename, format=None):
        """Read a graph from file."""
        self.graph = ig.Graph.Read(filename, format=format)

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
        # NetworkX is used to read the data and then the graph is converted to igraph
        G = nx.read_edgelist(
            filename,
            comments=comments,
            delimiter=delimiter,
            create_using=create_using,
            nodetype=nodetype,
            data=data,
            encoding=encoding,
        )
        self.graph = ig.Graph.from_networkx(G)
        self.graph.vs["name"] = self.graph.vs["_nx_name"]

    def read_adjacency(self, filename, index_col=0, create_using=nx.Graph):
        """Load network from CSV file with interdependency matrix."""
        # NetworkX is used to read the data and then the graph is converted to igraph
        if pathlib.Path(filename).suffix == ".csv":
            df = pd.read_csv(filename, index_col=index_col)
            # need to make sure dependency is interpreted as j --> i
            G = nx.from_pandas_adjacency(df.transpose(), create_using=create_using)
            self.graph = ig.Graph.from_networkx(G)
            self.graph.vs["name"] = self.graph.vs["_nx_name"]
        else:
            self.graph = None

    def write_gml(self, filename):
        """Write graph to GML file."""
        self.graph.write_gml(filename)

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

    def plot(self, **visual_style):
        ig.plot(self.graph, **visual_style)
