# -*- coding: utf-8 -*-
#
# parsing the hp.obo.

import re
import sys
sys.path.insert(0, 'util/')


import opfiles
import readwrite
import magicsplit

class Node(object):
    def __init__(self, line):
        super(Node, self).__init__()
        self.id = line[0]
        self.name = line[1]
        self.defi = line[2]
        self.is_a = line[3]
        self.synonym = line[4]
        self.alt_id = line[5]


def clean_data(lines):
    # remove header
    lines = lines[25:]
    # split list by "\n"
    splited_lines = magicsplit.magicsplit(lines, "\n")
    return splited_lines


def parsing(lines):
    want_to_extract = ["id", "name", "def", "is_a", "synonym", "alt_id"]
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
        elif "alt_id" in sl[0]:
            extracted[sl[0]] = extracted.get(sl[0], []) + [sl[2].strip(), ]
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
    """
    id::name::alt_id::definition::synonym::is_a
    """
    opfiles.is_file_exist(out_path, debug=True)

    with open(out_path, 'a') as wo:
        for node in nodes.values():
            out_str = (node.id + "::" + node.name + "::" +
                       ",".join(node.alt_id) + "::" +
                       node.defi + "::" + ",".join(node.synonym) + "::" +
                       ",".join(map(lambda n: n.id, node.is_a)) + "\n")
            try:
                wo.write(out_str.encode("utf-8"))
            except:
                print out_str


def output_name(names, out_path):
    opfiles.is_file_exist(out_path, debug=True)
    out_string = "\n".join(names)
    readwrite.write_to_txt(out_string, out_path, type="a")

    with open(out_path, 'a') as wo:
        out = "\n".join(names)
        wo.write(out.encode("utf-8").lower())


def filter_by_name_length(names):
    return filter(lambda name: len(name.strip("\n").split(" ")) <= 4, names)


def parsing_and_clean():
    path = "data/graph/humanphenotype.obo"
    out_all_path = "data/graph/parsed_hp"
    out_name_path = "data/graph/parsed_name"
    out_filtered_name_path = "data/graph/parsed_filtered_name"
    lines = readwrite.read_from_txt(path)
    cleaned_lines = clean_data(lines)
    parsed_lines = parsing(cleaned_lines)
    nodes = build_nodes(parsed_lines)
    names = extract_names(nodes)
    output_data(nodes, out_all_path)
    output_name(names, out_name_path)

    filtered_name = filter_by_name_length(names)
    output_name(filtered_name, out_filtered_name_path)


if __name__ == '__main__':
    parsing_and_clean()
