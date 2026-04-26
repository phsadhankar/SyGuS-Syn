import csv
import os
import time
from typing import Dict, List, Optional

from evaluator import candidate_passes_examples
from enumerator import BottomUpEnumerator
from verifier import Z3Verifier


def max2_spec(env: Dict[str, int], output: int) -> bool:
    x = env["x"]
    y = env["y"]

    return output >= x and output >= y and (output == x or output == y)


class CEGISSolver:
    def __init__(self, max_size=7, timeout_seconds=30):
        self.max_size = max_size
        self.timeout_seconds = timeout_seconds
        self.examples: List[Dict[str, int]] = [
            {"x": 0, "y": 0},
            {"x": 0, "y": 1},
            {"x": 1, "y": 0},
        ]

        self.iterations = 0
        self.generated_candidates = 0
        self.checked_candidates = 0
        self.start_time = None

    def solve_max2(self) -> Optional[str]:
        self.start_time = time.time()

        enumerator = BottomUpEnumerator(
            variable_names=["x", "y"],
            constants=[0, 1],
            max_size=self.max_size,
        )

        verifier = Z3Verifier(variable_names=["x", "y"])

        print("Starting CEGIS solver for max2(x, y)")
        print("Initial examples:", self.examples)
        print()

        for candidate in enumerator.enumerate():
            self.generated_candidates = enumerator.generated_count

            if time.time() - self.start_time > self.timeout_seconds:
                print("Timeout reached.")
                self.save_results(success=False, solution=None)
                return None

            if not candidate_passes_examples(candidate, self.examples, max2_spec):
                continue

            self.checked_candidates += 1
            self.iterations += 1

            print(f"CEGIS iteration {self.iterations}")
            print(f"Candidate: {candidate}")

            valid, counterexample = verifier.verify_max2(candidate)

            if valid:
                runtime = time.time() - self.start_time
                print()
                print("Solution found!")
                print(f"Synthesized expression: {candidate}")
                print(f"Runtime: {runtime:.4f} seconds")
                print(f"Candidates generated: {self.generated_candidates}")
                print(f"Candidates checked by Z3: {self.checked_candidates}")
                print(f"CEGIS iterations: {self.iterations}")

                self.save_results(success=True, solution=str(candidate))
                return str(candidate)

            print(f"Counterexample found: {counterexample}")
            print()

            if counterexample not in self.examples:
                self.examples.append(counterexample)

        print("No solution found within max expression size.")
        self.save_results(success=False, solution=None)
        return None

    def save_results(self, success: bool, solution: Optional[str]):
        os.makedirs("results", exist_ok=True)

        file_path = "results/results.csv"
        file_exists = os.path.exists(file_path)

        runtime = time.time() - self.start_time if self.start_time else 0

        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "benchmark",
                    "success",
                    "solution",
                    "runtime_seconds",
                    "generated_candidates",
                    "z3_checked_candidates",
                    "cegis_iterations",
                    "num_examples",
                    "max_size",
                ])

            writer.writerow([
                "max2",
                success,
                solution if solution else "",
                f"{runtime:.4f}",
                self.generated_candidates,
                self.checked_candidates,
                self.iterations,
                len(self.examples),
                self.max_size,
            ])
