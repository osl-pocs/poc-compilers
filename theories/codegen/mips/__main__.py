from cli import parse_cli
from mips import MathMIPS


if __name__ == "__main__":
    cli_args = parse_cli()

    expr = cli_args.expr

    mips = MathMIPS()

    mips.codegen(expr)
    print(mips.execute(verbose=True))