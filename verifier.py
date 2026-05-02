from __future__ import annotations

from typing import Dict, Optional, Tuple
import z3

from ast_nodes import Expr
from spec import constraint_to_z3
from sygus_parser import SyGuSBenchmark


class Z3Verifier:
    def __init__(self, bench: SyGuSBenchmark):
        self.bench = bench

    def verify(self, candidate: Expr) -> Tuple[bool, Optional[Dict[str, int]]]:
        z3_vars = {
            name: z3.Int(name)
            for name in self.bench.variable_names
        }

        constraints = [
            constraint_to_z3(c, self.bench, candidate, z3_vars)
            for c in self.bench.constraints
        ]

        solver = z3.Solver()
        solver.add(z3.Not(z3.And(*constraints)))

        result = solver.check()

        if result == z3.unsat:
            return True, None

        if result == z3.sat:
            model = solver.model()
            counterexample: Dict[str, int] = {}

            for name in self.bench.variable_names:
                value = model.eval(z3_vars[name], model_completion=True)
                counterexample[name] = value.as_long()

            return False, counterexample

        raise RuntimeError("Z3 returned unknown. Try simplifying the benchmark or increasing timeout.")
