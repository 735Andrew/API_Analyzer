import argparse
import sys

parser = argparse.ArgumentParser(
    description="Compares binary packages between two ALT Linux branches.",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "--branches",
    "-b",
    nargs=2,
    default=["sisyphus", "p10"],
    help="Names of two ALT Linux branches to compare.\n"
    "Example: python3 main.py -b sisyphus p10\n",
)

parser.add_argument(
    "--output",
    "-o",
    default="terminal",
    help="Output type.\n"
    "Example №1: python3 main.py -o data.txt\n"
    "Example №2: python3 main.py -o terminal\n",
)

namespace = parser.parse_args(sys.argv[1:])
