import sys

from amr import JAMR_AMR_Reader
from style import HTML_AMR

amr_pairs = {}

def style(assign_node_color=None, assign_node_desc=None, assign_edge_color=None, assign_edge_desc=None,
          assign_token_color=None, assign_token_desc=None):
    output = '<!DOCTYPE html>\n'
    output += '<html>\n'
    output += '<style>\n'
    output += HTML_AMR.style_sheet()
    output += '</style>\n\n'
    output += '<body>\n'
    for id  in amr_pairs:
        amr1, amr2 = amr_pairs[id]
        output += '1:\n'
        output += HTML_AMR.html(amr1,
                                assign_node_color, assign_node_desc,
                                assign_edge_color, assign_edge_desc,
                                assign_token_color, assign_token_desc)
        output += '2:\n'
        output += HTML_AMR.html(amr2,
                                assign_node_color, assign_node_desc,
                                assign_edge_color, assign_edge_desc,
                                assign_token_color, assign_token_desc)
    output += '</body>\n'
    output += '</html>\n'
    return output


def is_correct_node(amr, n):
    amr1, amr2 = amr_pairs[amr.id]
    node = amr.nodes[n]
    amr1_nodes = [amr1.nodes[m] for m in amr1.nodes]
    amr2_nodes = [amr2.nodes[m] for m in amr2.nodes]
    if node in amr1_nodes and node in amr2_nodes:
        return 'green'
    return 'red'

def is_correct_edge(amr, e):
    amr1, amr2 = amr_pairs[amr.id]
    s,r,t = e
    edge = (amr.nodes[s],r,amr.nodes[t])
    amr1_edges = [(amr1.nodes[s2],r2,amr1.nodes[t2]) for s2,r2,t2 in amr1.edges]
    amr2_edges = [(amr2.nodes[s2],r2,amr2.nodes[t2]) for s2,r2,t2 in amr2.edges]
    if edge in amr1_edges and edge in amr2_edges:
        return 'green'
    return 'red'


def is_correct_node_desc(amr, n):
    amr1, amr2 = amr_pairs[amr.id]
    node = amr.nodes[n]
    amr1_nodes = [amr1.nodes[m] for m in amr1.nodes]
    amr2_nodes = [amr2.nodes[m] for m in amr2.nodes]
    if node in amr1_nodes and node in amr2_nodes:
        return f'node ({amr.nodes[n]} in AMR 1 and AMR 2'
    return f'node ({amr.nodes[n]} missing from other AMR'

def is_correct_edge_desc(amr, e):
    amr1, amr2 = amr_pairs[amr.id]
    s,r,t = e
    edge = (amr.nodes[s],r,amr.nodes[t])
    amr1_edges = [(amr1.nodes[s2],r2,amr1.nodes[t2]) for s2,r2,t2 in amr1.edges]
    amr2_edges = [(amr2.nodes[s2],r2,amr2.nodes[t2]) for s2,r2,t2 in amr2.edges]
    if edge in amr1_edges and edge in amr2_edges:
        return f'edge ({amr.nodes[s]},{r},{amr.nodes[t]}) in AMR 1 and AMR 2'
    return f'edge ({amr.nodes[s]},{r},{amr.nodes[t]}) missing from other AMR'

def main():
    global amr_pairs
    import argparse

    parser = argparse.ArgumentParser(description='Visually compare two AMR files')
    parser.add_argument('files', type=str, nargs=2, required=True,
                        help='input files (AMRs in JAMR format)')
    parser.add_argument('output', type=str, required=True,
                        help='output file (html)')
    args = parser.parse_args()

    file1 = args.files[0]
    file2 = args.files[1]
    outfile = args.output

    cr = JAMR_AMR_Reader()
    amrs1 = cr.load(file1, verbose=False, remove_wiki=True)
    amrs2 = cr.load(file2, verbose=False, remove_wiki=True)
    for amr1, amr2 in zip(amrs1, amrs2):
        amr2.id = amr1.id
        amr_pairs[amr1.id] = (amr1,amr2)
    output = style(assign_node_color=is_correct_node,
                   assign_node_desc=is_correct_node_desc,
                   assign_edge_color=is_correct_edge,
                   assign_edge_desc=is_correct_edge_desc)

    with open(outfile, 'w+', encoding='utf8') as f:
        f.write(output)


if __name__=='__main__':
    main()