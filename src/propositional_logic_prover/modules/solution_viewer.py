from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter
from modules.clause import Clause


def build_derivation_tree(
    derivation: dict[Clause, tuple[Clause, Clause]]
) -> Node:
    root = Node("")
    nodes: list[Node] = [root]
    clauses: list[Clause] = [frozenset()]
    while clauses != []:
        node = nodes.pop()
        clause = clauses.pop()
        node.name = clause_to_str(clause)
        if clause not in derivation.keys():
            continue

        node.children = [Node(""), Node("")]
        nodes.extend(node.children)
        pair = derivation[clause]
        clauses.extend(pair)
    return root


def clause_to_str(clause: Clause) -> str:
    if len(clause) > 0:
        return ", ".join(clause)

    return "□"


def show_derivation(root: Node) -> None:
    for pre, _, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


def save_derivation_png(root: Node, path: str) -> None:
    # Turn graph bottom up and redirect edges back to parent
    UniqueDotExporter(
        root,
        options=[
            'rankdir="BT"',
            'edge [dir="back"]',
            'node [shape="box"]',
        ],
    ).to_picture(path)
