# -*- coding: utf-8 -*-
#
# using the predifined relationship to build a graph.

import logging
from snap import *
import igraph

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def read_parsed_hp_from_file(in_path):
    with open(in_path, "r") as f:
        return f.readlines()


def extract_info_from_parsed_hp(path):
    output_edge = path + "hp_edge_list.txt"
    output_id = path + "hp_name_list.txt"
    output_edge_str = ""
    output_id_str = ""
    id_map_name = {}
    lines = read_parsed_hp_from_file(path + "parsed_hp")

    for line in lines:
        elements = line.strip("\n").split("::")
        id = elements[0]
        name = elements[1]
        isas = elements[-1].split(",")
        output_id_str += id + "\t" + name + "\n"
        id_map_name[int(id)] = name

        for isa in isas:
            output_edge_str += id + "\t" + isa + "\n"

    with open(output_edge, "w") as o:
        o.write(output_edge_str.encode("utf-8"))

    with open(output_id, "w") as o:
        o.write(output_id_str.encode("utf-8"))
    return id_map_name


def build_snap_graph(path):
    outpath = path + "hp_edge_list.txt"
    graph = LoadEdgeList(PNEANet, outpath, 0, 1)
    return graph


def extract_edges(path, id_map_vid):
    mapping = lambda x: id_map_vid[int(x)]
    with open(path, "r") as o:
        lines = o.readlines()
    directions = []
    for line in lines:
        split_line = line.strip("\n").split("\t")
        if split_line[1] != "" and split_line[0] != "":
            directions.append((mapping(split_line[0]), mapping(split_line[1])))
    return directions


def map_id_to_vid(ids):
    vids = xrange(0, len(ids))
    return vids, dict(zip(ids, vids))


def build_igraph(id_map_name, path):
    ids = list(id_map_name.keys())
    vids, id_map_vid = map_id_to_vid(ids)
    graph = igraph.Graph().as_directed()
    graph.add_vertices(vids)
    directed_edges = extract_edges(path + "hp_edge_list.txt", id_map_vid)
    graph.add_edges(directed_edges)
    return graph
