# Copyright (c) 2024 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import unittest
import networkx as nx
import igraph as ig
import operator
import lnad.analysis as lnad


class TestLNAD(unittest.TestCase):
    def test_degree_centrality(self):
        G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
        N = lnad.NetworkAnalysis(ig.Graph.from_networkx(G))
        nx_deg = nx.degree_centrality(G)
        ig_deg = N.degree_centrality()
        for nx_d, ig_d in zip(nx_deg.values(), ig_deg.values()):
            self.assertAlmostEqual(nx_d, ig_d)

    def test_eigenvector_centrality(self):
        G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
        N = lnad.NetworkAnalysis(ig.Graph.from_networkx(G))
        nx_deg = nx.eigenvector_centrality(G)
        nx_deg = dict(sorted(nx_deg.items(), key=operator.itemgetter(1), reverse=True))
        ig_deg = N.eigenvector_centrality()
        for nx_d, ig_d in zip(nx_deg.values(), ig_deg.values()):
            self.assertAlmostEqual(nx_d, ig_d)

    def test_betweenness_centrality(self):
        G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
        N = lnad.NetworkAnalysis(ig.Graph.from_networkx(G))
        nx_deg = nx.betweenness_centrality(G)
        nx_deg = dict(sorted(nx_deg.items(), key=operator.itemgetter(1), reverse=True))
        ig_deg = N.betweenness_centrality()
        for nx_d, ig_d in zip(nx_deg.values(), ig_deg.values()):
            self.assertAlmostEqual(nx_d, ig_d)

    def test_edge_betweenness_centrality(self):
        G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
        N = lnad.NetworkAnalysis(ig.Graph.from_networkx(G))
        nx_deg = nx.edge_betweenness_centrality(G)
        nx_deg = dict(sorted(nx_deg.items(), key=operator.itemgetter(1), reverse=True))
        ig_deg = N.edge_betweenness_centrality()
        for nx_d, ig_d in zip(nx_deg.values(), ig_deg.values()):
            self.assertAlmostEqual(nx_d, ig_d)

    def test_closeness_centrality(self):
        G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
        N = lnad.NetworkAnalysis(ig.Graph.from_networkx(G))
        nx_deg = nx.closeness_centrality(G)
        nx_deg = dict(sorted(nx_deg.items(), key=operator.itemgetter(1), reverse=True))
        ig_deg = N.closeness_centrality()
        for nx_d, ig_d in zip(nx_deg.values(), ig_deg.values()):
            self.assertAlmostEqual(nx_d, ig_d)

    def test_pagerank(self):
        G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
        N = lnad.NetworkAnalysis(ig.Graph.from_networkx(G))
        nx_deg = nx.pagerank(G)
        nx_deg = dict(sorted(nx_deg.items(), key=operator.itemgetter(1), reverse=True))
        ig_deg = N.pagerank()
        for nx_d, ig_d in zip(nx_deg.values(), ig_deg.values()):
            self.assertAlmostEqual(nx_d, ig_d, places=6)

    def test_global_effectivness(self):
        G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
        N = lnad.NetworkAnalysis(ig.Graph.from_networkx(G))
        nx_eff = nx.global_efficiency(G)
        ig_eff = N.global_efficiency()
        self.assertAlmostEqual(nx_eff, ig_eff)

    def test_largest_connected_component(self):
        G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
        N = lnad.NetworkAnalysis(ig.Graph.from_networkx(G))
        nx_lcc = len(max(nx.connected_components(G), key=len))
        ig_lcc = N.largest_connected_component()
        self.assertEqual(nx_lcc, ig_lcc)


if __name__ == "__main__":
    unittest.main()
