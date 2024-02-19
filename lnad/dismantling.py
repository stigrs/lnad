# Copyright (c) 2024 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Provides methods for network dismantling."""

import copy
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import lnad.analysis as lnad


def plot_attack_results(
    nattacks,
    E_target,
    E_random_avg,
    E_random_std,
    xlabel,
    ylabel,
    attack_labels=["targeted", "random"],
    filename=None,
    dpi=300,
):
    """Function for plotting attack results."""
    _, ax = plt.subplots()

    ax.plot(nattacks, E_target, "-bo", label=attack_labels[0])
    ax.plot(nattacks, E_random_avg, "--r^", label=attack_labels[1])
    ax.fill_between(
        nattacks,
        E_random_avg - E_random_std,
        np.clip(E_random_avg + E_random_std, a_min=0.0, a_max=1.0),
        alpha=0.2,
        color="gray",
    )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

    # Put a legend below current axis
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox=True, ncol=2)

    if filename:
        plt.savefig(filename, dpi=dpi)

    return ax


class NetworkDismantling:
    """Class for carrying out network dismantling."""
    def __init__(self, G):
        self.graph = G

    def get_graph(self):
        return copy.deepcopy(self.graph)

    def node_iterative_centrality_attack(
        self, nattacks=1, weight=None, centrality_method=lnad.betweenness_centrality
    ):
        """Carry out iterative targeted attack on nodes.

        Arguments:
            nattacks: Number of attacks to be carried out
            weight: If weight is not none, use weighted centrality and efficiency measures
            centrality_method: Measure used for assessing the centrality of the nodes

        Reference:
            Petter Holme, Beom Jun Kim, Chang No Yoon, and Seung Kee Han
            Phys. Rev. E 65, 056109. https://arxiv.org/abs/cond-mat/0202410v1
        """
        if nattacks < 1:
            nattacks = 1
        if nattacks > self.graph.vcount():
            nattacks = self.graph.vcount()

        graph_attacked = self.get_graph()  # work on a local copy of the network
        nodes_attacked = [0]  # list with coordinates of attacked nodes
        centrality = [0]  # list with centralities of attacked nodes

        lcc = [lnad.largest_connected_component(graph_attacked)]
        slcc = [lnad.second_largest_connected_component(graph_attacked)]
        eff = [lnad.global_efficiency(graph_attacked, weight)]

        for _ in range(nattacks):
            bc = centrality_method(graph_attacked, weight)
            node = list(bc.keys())[0]
            graph_attacked.delete_vertices(node)
            nodes_attacked.append(node)
            lcc.append(lnad.largest_connected_component(graph_attacked))
            slcc.append(lnad.second_largest_connected_component(graph_attacked))
            eff.append(lnad.global_efficiency(graph_attacked, weight))
            centrality.append(list(bc.values())[0])

        return graph_attacked, nodes_attacked, lcc, slcc, eff, centrality

    def edge_iterative_centrality_attack(
        self,
        nattacks=1,
        weight=None,
        centrality_method=lnad.edge_betweenness_centrality,
    ):
        """Carry out iterative targeted attack on edges.

        Arguments:
            nattacks: Number of attacks to be carried out
            weight: If weight is not none, use weighted centrality and efficiency measures
            centrality_method: Measure used for assessing the centrality of the nodes

        Reference:
            Bellingeri, M., Bevacqua, D., Scotognella, F. et al. A comparative analysis of
            link removal strategies in real complex weighted networks.
            Sci Rep 10, 3911 (2020). https://doi.org/10.1038/s41598-020-60298-7
        """
        if nattacks < 1:
            nattacks = 1
        if nattacks > self.graph.ecount():
            nattacks = self.graph.ecount()

        graph_attacked = self.get_graph()  # work on a local copy of the topology
        edges_attacked = [0]  # list with coordinates of attacked edges
        centrality = [0]  # list with centralities of attacked nodes

        lcc = [lnad.largest_connected_component(graph_attacked)]
        slcc = [lnad.second_largest_connected_component(graph_attacked)]
        eff = [lnad.global_efficiency(graph_attacked, weight)]

        for _ in range(nattacks):
            bc = centrality_method(graph_attacked, weight)
            edge = list(bc.keys())[0]
            graph_attacked.delete_edges(edge)
            edges_attacked.append(edge)
            lcc.append(lnad.largest_connected_component(graph_attacked))
            slcc.append(lnad.second_largest_connected_component(graph_attacked))
            eff.append(lnad.global_efficiency(graph_attacked, weight))
            centrality.append(list(bc.values())[0])

        return graph_attacked, edges_attacked, lcc, slcc, eff, centrality

    def articulation_point_targeted_attack(self, nattacks=1, weight=None):
        """Carry out brute-force articulation point-targeted attack.

        Arguments:
            nattacks: Number of attacks to be carried out

        Reference:
            Tian, L., Bashan, A., Shi, DN. et al. Articulation points in complex networks.
            Nat Commun 8, 14223 (2017). https://doi.org/10.1038/ncomms14223
        """
        graph_attacked = self.get_graph()
        nodes_attacked = []  # list with coordinates of attacked nodes

        ap = lnad.articulation_points(graph_attacked)

        if nattacks < 1:
            nattacks = 1
        if nattacks > graph_attacked.vcount():
            nattacks = graph_attacked.vcount()

        lcc = [lnad.largest_connected_component(graph_attacked)]
        slcc = [lnad.second_largest_connected_component(graph_attacked)]
        eff = [lnad.global_efficiency(graph_attacked)]

        for i in range(nattacks):
            graph_attacked.delete_vertices(ap[i])
            nodes_attacked.append(ap[i])
            lcc.append(lnad.largest_connected_component(graph_attacked))
            slcc.append(lnad.second_largest_connected_component(graph_attacked))
            eff.append(lnad.global_efficiency(graph_attacked, weight))

        return graph_attacked, nodes_attacked, lcc, slcc, eff

    def random_attack(self, nattacks=1, weight=None):
        """Carry out random attack on nodes.

        Arguments:
            nattacks: Number of attacks to be carried out
            weighted: If weighted is not none, use weighted efficiency measure
        """
        if nattacks < 1:
            nattacks = 1
        if nattacks > self.graph.vcount():
            nattacks = self.graph.vcount()

        graph_attacked = self.get_graph()  # work on a local copy of the topology
        nodes_attacked = [0]  # list with coordinates of attacked nodes

        lcc = [lnad.largest_connected_component(graph_attacked)]
        slcc = [lnad.second_largest_connected_component(graph_attacked)]
        eff = [lnad.global_efficiency(graph_attacked, weight)]

        for _ in range(nattacks):
            node = rd.sample(list(graph_attacked.vs), 1)
            graph_attacked.delete_vertices(node[0])
            nodes_attacked.append(node[0])
            lcc.append(lnad.largest_connected_component(graph_attacked))
            slcc.append(lnad.second_largest_connected_component(graph_attacked))
            eff.append(lnad.global_efficiency(graph_attacked, weight))

        return graph_attacked, nodes_attacked, lcc, slcc, eff

    def edge_random_attack(self, nattacks=1, weight=None):
        """Carry out random attack on edges.

        Arguments:
            nattacks: Number of attacks to be carried out
            weighted: If weighted is not none, use weighted efficiency measure
        """
        if nattacks < 1:
            nattacks = 1
        if nattacks > self.graph.ecount():
            nattacks = self.graph.ecount()

        graph_attacked = self.get_graph()  # work on a local copy of the topology
        edges_attacked = [0]  # list with coordinates of attacked edges

        lcc = [lnad.largest_connected_component(graph_attacked)]
        slcc = [lnad.second_largest_connected_component(graph_attacked)]
        eff = [lnad.global_efficiency(graph_attacked, weight)]

        for _ in range(nattacks):
            edge = rd.sample(list(graph_attacked.es), 1)
            graph_attacked.delete_edges(edge[0])
            edges_attacked.append(edge[0])
            lcc.append(lnad.largest_connected_component(graph_attacked))
            slcc.append(lnad.second_largest_connected_component(graph_attacked))
            eff.append(lnad.global_efficiency(graph_attacked, weight))

        return graph_attacked, edges_attacked, lcc, slcc, eff
