import argparse

from cegis import CEGISSolver
from sygus_parser import parse_file


def main():
    parser = argparse.ArgumentParser(description="Minimal CEGIS-based SyGuS solver for small LIA benchmarks.")
    parser.add_argument("benchmark", nargs="?", default="benchmarks/max2.sl", help="Path to a .sl SyGuS benchmark file.")
    parser.add_argument("--max-size", type=int, default=9, help="Maximum expression size to enumerate.")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds.")
    args = parser.parse_args()

    benchmark = parse_file(args.benchmark)
    solver = CEGISSolver(benchmark, max_size=args.max_size, timeout_seconds=args.timeout)
    solution = solver.solve()

    print()
    if solution is None:
        print("Final answer: no solution found with current limits.")
    else:
        print(f"Final answer: {solution}")


if __name__ == "__main__":
    main()
