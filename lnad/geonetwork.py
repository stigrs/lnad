# Copyright (c) 2024 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Provides methods for handling networks with geographic data."""

import numpy as np
import networkx as nx
import pandas as pd
import geopandas as gpd
import contextily as ctx
import momepy
import pathlib
import copy
import matplotlib.pyplot as plt
from shapely import wkt


def plot_grid(
    grid,
    filename=None,
    figsize=(12, 12),
    dpi=300,
    xlabel="East",
    ylabel="North",
    add_basemap=False,
    provider=ctx.providers.OpenStreetMap.Mapnik,
    **kwargs
):
    """Plot original network grid."""
    _, ax = plt.subplots(figsize=figsize)
    grid.plot(ax=ax, **kwargs)
    if add_basemap:
        ctx.add_basemap(ax, crs=grid.crs, source=provider)
    plt.tight_layout()
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    if filename:
        plt.savefig(filename, dpi=dpi)
    return ax


def plot_grid_topology(graph, filename=None, figsize=(12, 12), node_size=5, dpi=300):
    """Plot network grid topology."""
    pos = {n: [n[0], n[1]] for n in list(graph.nodes)}
    _, _ = plt.subplots(figsize=figsize)
    nx.draw(graph, pos, node_size=node_size)
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=dpi)


class GeoNetwork:
    """Class for representing networks with geographic data."""
    def __init__(
        self, filename, multigraph=False, explode=False, capacity=None, epsg=None
    ):
        """Initialise network.

        Arguments:
            filename: name of file with geodata for the infrastructure grid
            multigraph: true if multigraph should be created
            explode: true if multilinestrings should be expanded
            epsg: transform to EPSG code
            capacity: string specifying the attribute with capacities for the edges
        """
        self.graph = None
        self.grid = None
        self.__multigraph = multigraph
        self.load(filename, multigraph, explode, capacity, epsg)

    def load(self, filename, multigraph=False, explode=False, capacity=None, epsg=None):
        """Load geodata for network from file (e.g. GEOJSON format)."""
        if pathlib.Path(filename).suffix == ".csv":
            df = pd.read_csv(filename)
            df["geometry"] = df["geometry"].apply(wkt.loads)
            self.grid = gpd.GeoDataFrame(df, crs=epsg)
        else:  # assume it is a format geopandas can read directly
            self.grid = gpd.read_file(filename)
            if epsg:
                self.grid.to_crs(epsg)
        self.__multigraph = multigraph
        if explode:
            self.grid = self.grid.explode()
        if capacity:
            # avoid division by zero, NaN or Inf
            self.grid[capacity] = self.grid[capacity].replace(
                to_replace=np.inf, value=np.finfo(float).max
            )
            self.grid[capacity] = self.grid[capacity].replace(
                to_replace=np.nan, value=np.finfo(float).eps
            )
            self.grid[capacity] = self.grid[capacity].replace(
                to_replace=0.0, value=np.finfo(float).eps
            )
            # shortest path weights are calculated as the resiprocal of the capacity
            self.grid["weight"] = 1.0 / self.grid[capacity]
        self.graph = momepy.gdf_to_nx(self.grid, multigraph=multigraph, directed=False)

    def get_graph(self):
        """Return a deep copy of the graph."""
        return copy.deepcopy(self.graph)

    def remove_false_nodes(self):
        """Clean topology of existing LineString geometry by removal of nodes of degree 2."""
        self.grid = momepy.remove_false_nodes(self.grid)
        self.graph = momepy.gdf_to_nx(
            self.grid, multigraph=self.__multigraph, directed=False
        )

    def close_gaps(self, tolerance):
        """Close gaps in LineString geometry where it should be contiguous.
        Snaps both lines to a centroid of a gap in between."""
        self.grid.geometry = momepy.close_gaps(self.grid, tolerance)
        self.graph = momepy.gdf_to_nx(
            self.grid, multigraph=self.__multigraph, directed=False
        )

    def extend_lines(self, tolerance):
        """Extends unjoined ends of LineString segments to join with other segments within
        a set tolerance."""
        self.grid = momepy.extend_lines(self.grid, tolerance)
        self.graph = momepy.gdf_to_nx(
            self.grid, multigraph=self.__multigraph, directed=False
        )

    def plot(
        self,
        filename=None,
        figsize=(12, 12),
        dpi=300,
        xlabel="East",
        ylabel="North",
        add_basemap=False,
        provider=ctx.providers.OpenStreetMap.Mapnik,
        **kwargs
    ):
        """Plot original network grid."""
        return plot_grid(
            self.grid,
            filename,
            figsize,
            dpi,
            xlabel,
            ylabel,
            add_basemap,
            provider,
            **kwargs
        )

    def plot_topology(self, filename=None, figsize=(12, 12), node_size=5, dpi=300):
        """Plot graph of network topology."""
        plot_grid_topology(self.graph, filename, figsize, node_size, dpi)
