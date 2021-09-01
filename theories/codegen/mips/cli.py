import argparse


def parse_cli():
    parser = argparse.ArgumentParser(
        description=(
            "MathMIPS process a simple math string and convert it to AST or "
            "to MIPS code."
        )
    )
    parser.add_argument(
        "--ast",
        action="store",
        type=bool,
        default=False,
        help="Return AST for the given expression.",
    )
    parser.add_argument(
        "--codegen",
        action="store",
        type=bool,
        default=True,
        help="Return the MIPS code for the given expression.",
    )
    parser.add_argument(
        'expr', 
        metavar='N',
        type=str,
        help='expr to be compiled.'
    )
    return parser.parse_args()