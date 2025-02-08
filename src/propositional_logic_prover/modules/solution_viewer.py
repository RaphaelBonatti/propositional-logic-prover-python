from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter
from modules.clause import Clause


class DerivationBuilder:
    def __init__(
        self, derivation_map: dict[Clause, tuple[Clause, Clause]]
    ) -> None:
        self._derivation_map: dict[Clause, tuple[Clause, Clause]] = (
            derivation_map
        )

    def create_node(self, clause: Clause) -> Node:
        if clause in self._derivation_map.keys():
            clause1, clause2 = self._derivation_map[clause]
            node_lhs = self.create_node(clause1)
            node_rhs = self.create_node(clause2)
            return Node(clause_to_str(clause), children=[node_lhs, node_rhs])

        return Node(clause_to_str(clause))

    def build(self) -> Node:
        return self.create_node(frozenset())


def clause_to_str(clause: Clause) -> str:
    if len(clause) > 0:
        return ", ".join(clause)

    return "□"


def show_derivation(node: Node) -> None:
    for pre, _, node in RenderTree(node):
        print("%s%s" % (pre, node.name))


def save_derivation_png(node: Node, path: str) -> None:
    # Turn graph bottom up and redirect edges back to parent
    UniqueDotExporter(
        node,
        options=[
            'rankdir="BT"',
            'edge [dir="back"]',
            'node [shape="box"]',
        ],
    ).to_picture(path)
