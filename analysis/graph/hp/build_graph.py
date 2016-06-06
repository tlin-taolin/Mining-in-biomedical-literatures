# -*- coding: utf-8 -*-
#
# using the predifined relationship to build a graph.

import sys
import logging
from snap import *
import igraph

sys.path.insert(0, 'util/')

import groupby
import readwrite


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def extract_info_from_parsed_hp(path):
    output_edge = path + "hp_edge_list.txt"
    output_id = path + "hp_name_list.txt"
    output_edge_str = ""
    output_id_str = ""
    id_map_name = {}
    lines = readwrite.read_from_txt(path + "parsed_hp")

    for line in lines:
        elements = line.strip("\n").split("::")
        id = elements[0]
        name = elements[1]
        alt_lids = elements[2]
        isas = elements[-1]
        id_map_name[int(id)] = name

        if len(isas) != 0:
            isas = isas.split(",")
            for isa in isas:
                output_edge_str += isa + "\t" + id + "\n"
                if len(alt_lids) != 0:
                    alt_ids = alt_lids.split(",")
                    for alt_id in alt_ids:
                        output_edge_str += alt_id + "\t" + isa + "\n"

        output_id_str += id + "\t" + name + "\n"

    with open(output_edge, "w") as o:
        o.write(output_edge_str.encode("utf-8"))

    with open(output_id, "w") as o:
        o.write(output_id_str.encode("utf-8"))
    return id_map_name


def extract_adjlist(path):
    lines = readwrite.read_from_txt(path)
    edges = [line.strip("\n").split("\t") for line in lines]
    grouped_edges = groupby.group_by(edges, index=0)
    extract = lambda x: x[1]
    return dict([(k, map(extract, v)) for k, v in grouped_edges])


def build_snap_graph(path):
    outpath = path + "hp_edge_list.txt"
    graph = LoadEdgeList(PNEANet, outpath, 0, 1)
    return graph


def extract_edges(path, id_map_vid):
    mapping = lambda x: id_map_vid[int(x)]
    lines = readwrite.read_from_txt(path)

    directions = []
    for line in lines:
        split_line = line.strip("\n").split("\t")
        if split_line[1] != "" and split_line[0] != "":
            try:
                directions.append((mapping(split_line[0]), mapping(split_line[1])))
            except:
                pass
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
