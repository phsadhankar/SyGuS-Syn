import csv
import time
from pathlib import Path

from cegis import CEGISSolver
from sygus_parser import parse_file


BENCHMARK_DIR = Path("benchmarks")
RESULTS_FILE = Path("results/batch_results.csv")

MAX_SIZE = 13
TIMEOUT = 30


FIELDNAMES = [
    "benchmark",
    "status",
    "solution",
    "runtime",
    "generated",
    "checked",
    "iterations",
    "examples",
    "error",
]


def run_benchmark(file_path):
    row = {
        "benchmark": file_path.name,
        "status": "",
        "solution": "",
        "runtime": "",
        "generated": "",
        "checked": "",
        "iterations": "",
        "examples": "",
        "error": "",
    }

    try:
        bench = parse_file(str(file_path))

        solver = CEGISSolver(
            bench,
            max_size=MAX_SIZE,
            timeout_seconds=TIMEOUT,
        )

        start = time.time()
        solution = solver.solve()
        runtime = time.time() - start

        row["runtime"] = round(runtime, 4)
        row["generated"] = solver.generated_candidates
        row["checked"] = solver.z3_checked_candidates
        row["iterations"] = solver.cegis_iterations
        row["examples"] = len(solver.examples)

        if solution is None:
            row["status"] = "timeout_or_fail"
        else:
            row["status"] = "success"
            row["solution"] = str(solution)

    except Exception as e:
        row["status"] = "error"
        row["error"] = str(e)

    return row


def main():
    RESULTS_FILE.parent.mkdir(exist_ok=True)

    files = sorted(BENCHMARK_DIR.glob("*.sl"))

    print(f"Looking in: {BENCHMARK_DIR.resolve()}")
    print(f"Found {len(files)} benchmarks\n")

    if not files:
        print("No .sl files found in benchmarks/.")
        print("Run: python generate_benchmarks.py")
        return

    results = []

    for file_path in files:
        print(f"Running: {file_path.name}")
        result = run_benchmark(file_path)
        results.append(result)
        print(f"Status: {result['status']}\n")

    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(results)

    success = sum(1 for r in results if r["status"] == "success")
    fail = sum(1 for r in results if r["status"] == "timeout_or_fail")
    errors = sum(1 for r in results if r["status"] == "error")

    print("===== SUMMARY =====")
    print(f"Total: {len(results)}")
    print(f"Success: {success}")
    print(f"Fail/Timeout: {fail}")
    print(f"Errors: {errors}")
    print(f"Results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()
