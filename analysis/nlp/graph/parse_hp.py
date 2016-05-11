# -*- coding: utf-8 -*-
#
# parsing the hp.obo.

import re
from node import Node
import os


def read_data(path):
    with open(path, "r") as r:
        return r.readlines()


def clean_data(lines):
    # remove header
    lines = lines[25:]
    # split list by "\n"
    splited_lines = magicsplit(lines, "\n")
    return splited_lines


def magicsplit(l, *splitters):
    return [subl for subl in _itersplit(l, splitters) if subl]


def _itersplit(l, splitters):
    current = []
    for item in l:
        if item in splitters:
            yield current
            current = []
        else:
            current.append(item)
    yield current


def parsing(lines):
    want_to_extract = ["id", "name", "def", "is_a", "synonym"]
    parsed_lines = []
    for line in lines:
        extracted_line = extract(line)
        final_line = [extracted_line.get(want, "") for want in want_to_extract]
        parsed_lines.append(final_line)
    return parsed_lines


def extract(line):
    extracted = {}
    for l in line[1: ]:
        l = l.strip("\n")
        sl = re.split(":", l)

        if "is_a" == sl[0]:
            tmp = re.split("!", sl[2])
            extracted[sl[0]] = extracted.get(sl[0], []) + [tmp[0].strip(), ]
        elif "id" in sl[0]:
            extracted[sl[0]] = sl[2].strip()
        elif "synonym" in sl[0]:
            extracted[sl[0]] = extracted.get(sl[0], []) + [re.split(r'"', sl[1])[1], ]
        elif "name" in sl[0]:
            extracted[sl[0]] = sl[1].strip()
        else:
            extracted[sl[0]] = sl[1].strip()
            try:
                extracted[sl[0]] = re.split(r'"', sl[1])[1]
            except:
                extracted[sl[0]] = sl[1].strip()
    return extracted


def build_nodes(lines):
    nodes = {line[0]: Node(line) for line in lines}

    for k, v in nodes.items():
        is_a = v.is_a
        if is_a:
            v.is_a = [nodes[n] for n in is_a]
    return nodes


def extract_names(nodes):
    return [v.name for v in nodes.values() if v.name != "All"]


def output_data(nodes, out_path):
    if os.path.exists(out_path):
        os.remove(out_path)

    with open(out_path, 'a') as wo:
        for node in nodes.values():
            out_str = (node.id + "::" + node.name + "::" + node.defi + "::" + ",".join(node.synonym) + "::" + ",".join(map(lambda n: n.id, node.is_a)) + "\n")
            try:
                wo.write(out_str.encode("utf-8"))
            except:
                print out_str


def output_name(names, out_path):
    if os.path.exists(out_path):
        os.remove(out_path)

    with open(out_path, 'a') as wo:
        out = "\n".join(names)
        wo.write(out.encode("utf-8"))


if __name__ == '__main__':
    path = "data/graph/humanphenotype.obo"
    out_all_path = "data/graph/parsed_hp"
    out_name_path = "data/graph/parsed_name"
    lines = read_data(path)
    cleaned_lines = clean_data(lines)
    parsed_lines = parsing(cleaned_lines)
    nodes = build_nodes(parsed_lines)
    names = extract_names(nodes)
    output_data(nodes, out_all_path)
    output_name(names, out_name_path)
