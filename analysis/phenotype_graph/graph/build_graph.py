# -*- coding: utf-8 -*-
#
# using the predifined relationship to build a graph.

from snap import *


class Node(object):
    def __init__(self, id, name, isa):
        super(Node, self).__init__()
        self.id = id
        self.name = name
        self.isa = isa


def read_parsed_hp_from_file(in_path):
    with open(in_path, "r") as f:
        return f.readlines()


def extract_info_from_parsed_hp(lines):
    nodes = dict()
    for line in lines:
        elements = line.split("::")
        id = int(elements[0])
        name = elements[1]
        isa = elements[4].strip("\n").split(",")
        nodes[id] = Node(id, name, isa)
    for key, value in nodes.items():
        value.isa = map(lambda x: nodes.get(x, ""), value.isa)
        nodes[key] = value
    return nodes


def extract_isa_from_nodes(nodes):
    return [(id, extract_isa_from_node(node)) for id, node in nodes.items()]


def extract_isa_from_node(node):
    try:
        ids = [int(n.id) for n in node.isa]
    except:
        ids = []
    return ids


def init_directed_graph():
    return TNGraph.New()


def init_undirected_graph():
    return TUNGraph.New()


def add_nodes_to_graph(nodes, graph):
    for id, isa_id in nodes:
        graph.AddNode(id)
    return graph


def add_edges_to_graph(nodes, graph):
    for id, isa_ids in nodes:
        for isa_id in isa_ids:
            graph.AddEdge(id, isa_id)
    return graph


def build_graph(nodes, init_graph=init_directed_graph()):
    graph = init_graph()
    graph = add_nodes_to_graph(nodes, graph)
    graph = add_edges_to_graph(nodes, graph)
    return graph


def plot_graph(graph):
    PlotInDegDistr(graph, "1", "2")
    DrawGViz(graph)


def main(path):
    lines = read_parsed_hp_from_file(path)
    nodes = extract_info_from_parsed_hp(lines)
    isa_nodes = extract_isa_from_nodes(nodes)
    graph = build_graph(isa_nodes)
    plot_graph(graph)

if __name__ == '__main__':
    data_path = "data/parsed_hp"
    main(data_path)
