import sys

from amr import JAMR_AMR_Reader, Graph_AMR_Reader
from style import HTML_AMR

amr_triples = {}
version = None

def style(file1, file2, assign_node_color=None, assign_node_desc=None, assign_edge_color=None, assign_edge_desc=None,
          assign_token_color=None, assign_token_desc=None):
    global version
    output = '<!DOCTYPE html>\n'
    output += '<html>\n'
    output += '<style>\n'
    output += HTML_AMR.style_sheet()
    output += '</style>\n\n'
    output += '<body>\n'
    for id  in amr_triples:
        amr1, amr2, gold_amr = amr_triples[id]
        version = 1
        output += f'1 {file1}:\n'
        output += HTML_AMR.html(amr1,
                                assign_node_color, assign_node_desc,
                                assign_edge_color, assign_edge_desc,
                                assign_token_color, assign_token_desc)
        version = 2
        output += f'2: {file2}\n'
        output += HTML_AMR.html(amr2,
                                assign_node_color, assign_node_desc,
                                assign_edge_color, assign_edge_desc,
                                assign_token_color, assign_token_desc)
        version = 3
        output += f'gold:\n'
        output += HTML_AMR.html(gold_amr,
                                assign_node_color, assign_node_desc,
                                assign_edge_color, assign_edge_desc,
                                assign_token_color, assign_token_desc)
    output += '</body>\n'
    output += '</html>\n'
    return output


def is_correct_node(amr, n):
    if version==3:
        return ''
    amr1, amr2, gold_amr = amr_triples[amr.id]
    other_amr = amr1 if version==2 else amr2
    node = amr.nodes[n]
    gold_nodes = [gold_amr.nodes[m] for m in gold_amr.nodes]
    other_nodes = [other_amr.nodes[m] for m in other_amr.nodes]
    if node in gold_nodes and node not in other_nodes:
        return 'green'
    if node not in gold_nodes and node not in other_nodes:
        return 'red'
    return ''

def is_correct_edge(amr, e):
    if version==3:
        return ''
    amr1, amr2, gold_amr = amr_triples[amr.id]
    other_amr = amr1 if version == 2 else amr2
    s,r,t = e
    edge = (amr.nodes[s],r,amr.nodes[t])
    gold_edges = [(gold_amr.nodes[s2],r2,gold_amr.nodes[t2]) for s2,r2,t2 in gold_amr.edges]
    other_edges = [(other_amr.nodes[s2],r2,other_amr.nodes[t2]) for s2,r2,t2 in other_amr.edges]
    if edge in gold_edges and edge not in other_edges:
        return 'green'
    if edge not in gold_edges and edge not in other_edges:
        return 'red'
    return ''


def main():
    global amr_triples
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    file3 = sys.argv[3]
    outfile = sys.argv[4]

    cr = JAMR_AMR_Reader()
    amrs1 = cr.load(file1, verbose=False, remove_wiki=True)
    gold_amrs = cr.load(file3, verbose=False, remove_wiki=True)
    cr = Graph_AMR_Reader()
    amrs2 = cr.load(file2, verbose=False, remove_wiki=True)
    for amr1, amr2, gold_amr in zip(amrs1, amrs2, gold_amrs):
        amr1.id = gold_amr.id
        amr2.id = gold_amr.id
        amr_triples[amr1.id] = (amr1, amr2, gold_amr)

    output = style(file1, file2, assign_node_color=is_correct_node,
                   assign_edge_color=is_correct_edge)

    with open(outfile, 'w+', encoding='utf8') as f:
        f.write(output)


if __name__=='__main__':
    main()
