import argparse # todo cli
import sys

parser = argparse.ArgumentParser()

parser.add_argument("files", nargs="+")
parser.add_argument("--report", "-r", default="payout")


namespace = parser.parse_args(sys.argv[1:])


# python main.py --branches sisyphus p10