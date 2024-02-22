# LNAD - Library for Network Analysis and Dismantling

Library for network analysis and dismantling.

## Documentation

Network analysis methods:

* Degree centrality
* Eigenvector centrality
* Betweenness centrality
* Edge betweenness centrality
* Closeness centrality
* Pagerank
* Articulation points
* Largest connected component
* Second largest connected component
* Global efficiency

Network dismantling methods:

* Iterative targeted attack on nodes
* Iterative targeted attack on edges
* Brute-force articulation point targeted attack
* Random attack on nodes
* Random attack on edges

References:

* Petter Holme, Beom Jun Kim, Chang No Yoon, and Seung Kee Han. Phys. Rev. E 65, 056109. https://arxiv.org/abs/cond-mat/0202410v1
* Bellingeri, M., Bevacqua, D., Scotognella, F. et al. A comparative analysis of link removal strategies in real complex weighted networks. Sci Rep 10, 3911 (2020). https://doi.org/10.1038/s41598-020-60298-7
* Tian, L., Bashan, A., Shi, DN. et al. Articulation points in complex networks. Nat Commun 8, 14223 (2017). https://doi.org/10.1038/ncomms14223

## Licensing

LNAD is released under the [MIT](LICENSE) license.

## Obtain the Code

The source code can be obtained from:

    git clone https://github.com/stigrs/lnad.git

## Installation

The program is install by executing:

    python -m pip install . --prefix=%USERPROFILE%
