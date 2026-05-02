import csv
import time
from pathlib import Path

from cegis import CEGISSolver
from sygus_parser import parse_file


BENCHMARK_DIR = Path("benchmarks")
RESULTS_FILE = Path("results/batch_results.csv")


MAX_SIZE = 10
TIMEOUT = 20   # seconds per benchmark


def run_benchmark(file_path):
    try:
        bench = parse_file(str(file_path))
    except Exception as e:
        return {
            "benchmark": file_path.name,
            "status": "parse_error",
            "error": str(e),
        }

    solver = CEGISSolver(
        bench,
        max_size=MAX_SIZE,
        timeout_seconds=TIMEOUT,
    )

    start = time.time()

    try:
        solution = solver.solve()
        runtime = time.time() - start

        if solution is None:
            status = "timeout_or_fail"
        else:
            status = "success"

        return {
            "benchmark": file_path.name,
            "status": status,
            "solution": str(solution) if solution else "",
            "runtime": round(runtime, 4),
            "generated": solver.generated_candidates,
            "checked": solver.z3_checked_candidates,
            "iterations": solver.cegis_iterations,
            "examples": len(solver.examples),
        }

    except Exception as e:
        return {
            "benchmark": file_path.name,
            "status": "error",
            "error": str(e),
        }


def main():
    RESULTS_FILE.parent.mkdir(exist_ok=True)

    files = sorted(BENCHMARK_DIR.glob("*.sl"))

    print(f"Found {len(files)} benchmarks\n")

    results = []

    for file in files:
        print(f"Running: {file.name}")

        result = run_benchmark(file)
        results.append(result)

        print(f"Status: {result['status']}\n")

    # write CSV
    with open(RESULTS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # summary
    success = sum(1 for r in results if r["status"] == "success")
    fail = sum(1 for r in results if r["status"] == "timeout_or_fail")
    errors = sum(1 for r in results if r["status"] in ["error", "parse_error"])

    print("===== SUMMARY =====")
    print(f"Total: {len(results)}")
    print(f"Success: {success}")
    print(f"Fail/Timeout: {fail}")
    print(f"Errors: {errors}")
    print(f"Results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()