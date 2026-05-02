from __future__ import annotations

import csv
import os
import time
from typing import Dict, List, Optional

from ast_nodes import Expr
from evaluator import candidate_passes_examples
from enumerator import BottomUpEnumerator
from sygus_parser import SyGuSBenchmark
from verifier import Z3Verifier


class CEGISSolver:
    def __init__(
        self,
        benchmark: SyGuSBenchmark,
        max_size: int = 9,
        timeout_seconds: int = 30,
    ):
        self.benchmark = benchmark
        self.max_size = max_size
        self.timeout_seconds = timeout_seconds

        self.examples: List[Dict[str, int]] = self._initial_examples()

        self.generated_candidates = 0
        self.z3_checked_candidates = 0
        self.cegis_iterations = 0
        self.start_time = 0.0

    def solve(self) -> Optional[Expr]:
        self.start_time = time.time()

        enumerator = BottomUpEnumerator(
            variable_names=self.benchmark.synth_args,
            constants=self.benchmark.constants,
            int_ops=self.benchmark.int_ops,
            bool_ops=self.benchmark.bool_ops,
            max_size=self.max_size,
        )

        verifier = Z3Verifier(self.benchmark)

        print(f"Benchmark: {self.benchmark.synth_name}")
        print(f"Variables: {self.benchmark.variable_names}")
        print(f"Constants: {self.benchmark.constants}")
        print(f"Int ops: {sorted(self.benchmark.int_ops)}")
        print(f"Bool ops: {sorted(self.benchmark.bool_ops)}")
        print(f"Initial examples: {self.examples}")
        print()

        for candidate in enumerator.enumerate():
            self.generated_candidates = enumerator.generated_count

            if time.time() - self.start_time > self.timeout_seconds:
                print("Timeout reached.")
                self._save_results(False, None)
                return None

            if not candidate_passes_examples(candidate, self.benchmark, self.examples):
                continue

            self.z3_checked_candidates += 1
            self.cegis_iterations += 1

            print(f"CEGIS iteration {self.cegis_iterations}")
            print(f"Candidate: {candidate}")

            valid, counterexample = verifier.verify(candidate)

            if valid:
                print()
                print("Solution found!")
                print(f"Synthesized expression: {candidate}")
                print(f"Runtime: {time.time() - self.start_time:.4f} seconds")
                print(f"Candidates generated: {self.generated_candidates}")
                print(f"Candidates checked by Z3: {self.z3_checked_candidates}")
                print(f"CEGIS iterations: {self.cegis_iterations}")

                self._save_results(True, str(candidate))
                return candidate

            print(f"Counterexample found: {counterexample}")
            print()

            if counterexample not in self.examples:
                self.examples.append(counterexample)

        print("No solution found within the chosen max expression size.")
        self._save_results(False, None)
        return None

    def _initial_examples(self) -> List[Dict[str, int]]:
        names = self.benchmark.variable_names
        examples: List[Dict[str, int]] = []

        if not names:
            return [{}]

        examples.append({name: 0 for name in names})

        for i, name in enumerate(names):
            env = {n: 0 for n in names}
            env[name] = [-1, 0, 1][i % 3]

            if env not in examples:
                examples.append(env)

        if len(names) == 2:
            extra = [
                {names[0]: 0, names[1]: 1},
                {names[0]: 1, names[1]: 0},
                {names[0]: -1, names[1]: 2},
            ]

            for env in extra:
                if env not in examples:
                    examples.append(env)

        return examples

    def _save_results(self, success: bool, solution: Optional[str]) -> None:
        os.makedirs("results", exist_ok=True)

        path = "results/results.csv"
        file_exists = os.path.exists(path)
        runtime = time.time() - self.start_time

        with open(path, "a", newline="", encoding="utf-8") as file:
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
                self.benchmark.synth_name,
                success,
                solution or "",
                f"{runtime:.4f}",
                self.generated_candidates,
                self.z3_checked_candidates,
                self.cegis_iterations,
                len(self.examples),
                self.max_size,
            ])
