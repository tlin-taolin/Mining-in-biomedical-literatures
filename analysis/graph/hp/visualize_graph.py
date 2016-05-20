# -*- coding: utf-8 -*-
#
# analyze the graph.

import logging
from snap import *


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def plot_snap_graph(graph):
    logging.info("Plot snap graph...")
    PlotInDegDistr(graph, "1", "Directed graph - in-degree Distribution")
    PlotOutDegDistr(graph, "1", "Directed graph - out-degree Distribution")
    # DrawGViz(graph, gvlDot, "graph.png", "graph 1")


def plot_igraph_graph(graph):
    logging.info("Plot igraph...")
    # layout1 = graph.layout("kk")
    # plot(g, 'graph.pdf', layout=layout1)
