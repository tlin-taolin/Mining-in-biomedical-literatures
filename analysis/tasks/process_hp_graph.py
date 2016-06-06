# -*- coding: utf-8 -*-
#
# all graph operation.

import sys
sys.path.insert(0, 'graph/hp/')

import build_graph
import analyze_graph
import visualize_graph


def main(path):
    id_map_name = build_graph.extract_info_from_parsed_hp(path)
    snap_graph = build_graph.build_snap_graph(path)
    analyze_graph.analyze_snap_graph(snap_graph, id_map_name)
    visualize_graph.plot_snap_graph(snap_graph)

    igraph_graph = build_graph.build_igraph(id_map_name, path)
    analyze_graph.analyze_igraph_graph(igraph_graph)
    visualize_graph.plot_igraph_graph(igraph_graph)


if __name__ == '__main__':
    data_path = "data/hp/"
    main(data_path)
