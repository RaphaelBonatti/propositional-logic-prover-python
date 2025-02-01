from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter
from modules.clause import Clause


class SolutionViewer:
    def __init__(
        self, derivation_map: dict[Clause, tuple[Clause, Clause]]
    ) -> None:
        self._derivation_map: dict[Clause, tuple[Clause, Clause]] = (
            derivation_map
        )
        self._node: Node = self._derive(frozenset())

    def _clause_to_str(self, clause: Clause) -> str:
        if len(clause) > 0:
            return ", ".join(clause)

        return "□"

    def _derive(self, clause: Clause) -> Node:
        if clause in self._derivation_map.keys():
            clause1, clause2 = self._derivation_map[clause]
            node_lhs = self._derive(clause1)
            node_rhs = self._derive(clause2)
            return Node(
                self._clause_to_str(clause), children=[node_lhs, node_rhs]
            )

        return Node(self._clause_to_str(clause))

    def show_derivation(self) -> None:
        for pre, _, node in RenderTree(self._node):
            print("%s%s" % (pre, node.name))

    def save_derivation_png(self, path: str) -> None:
        # Turn graph bottom up and redirect edges back to parent
        UniqueDotExporter(
            self._node,
            options=[
                'rankdir="BT"',
                'edge [dir="back"]',
                'node [shape="box"]',
            ],
        ).to_picture(path)
