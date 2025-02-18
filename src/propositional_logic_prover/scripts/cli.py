import argparse

from modules import solution_viewer, parser, prover


def parse_args():
    parser = argparse.ArgumentParser(
        prog="pltt-cli",
        description="Enter a WFF knowledge base and a WFF query as string and visualize the derivation if the query is logically entailed by the knowledge base.",
    )
    parser.add_argument("kb", type=str, help="knowledge base (as WFF)")
    parser.add_argument("query", type=str, help="query to prove (as WFF)")
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="print a formatted derivation",
    )
    parser.add_argument(
        "-g",
        "--generate",
        metavar="FILENAME",
        help="give a name and generate a derivation in png",
        type=str,
    )
    return parser.parse_args()


def entrypoint():
    args = parse_args()
    kb = parser.wff_from_str(args.kb)
    query = parser.wff_from_str(args.query)
    is_valid, derivation = prover.prove_by_refutation(kb, query)
    if not is_valid:
        print("The knowledge base does not entail the query.")
        return

    root = solution_viewer.build_derivation_tree(derivation)
    if args.print:
        solution_viewer.show_derivation(root)
    if args.generate:
        filename = args.generate
        solution_viewer.save_derivation_png(root, args.generate + ".png")
        print(f"The derivation {filename}.png has been generated.")


if __name__ == "__main__":
    entrypoint()
