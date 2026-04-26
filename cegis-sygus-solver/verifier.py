from typing import Dict, Optional, Tuple
import z3
from ast_nodes import Expr


class Z3Verifier:
    def __init__(self, variable_names=None):
        self.variable_names = variable_names or ["x", "y"]

    def verify_max2(self, candidate: Expr) -> Tuple[bool, Optional[Dict[str, int]]]:
        z3_vars = {name: z3.Int(name) for name in self.variable_names}

        x = z3_vars["x"]
        y = z3_vars["y"]

        candidate_z3 = candidate.to_z3(z3_vars)

        spec = z3.And(
            candidate_z3 >= x,
            candidate_z3 >= y,
            z3.Or(candidate_z3 == x, candidate_z3 == y),
        )

        solver = z3.Solver()
        solver.add(z3.Not(spec))

        result = solver.check()

        if result == z3.unsat:
            return True, None

        if result == z3.sat:
            model = solver.model()
            counterexample = {}

            for name in self.variable_names:
                value = model[z3_vars[name]]

                if value is None:
                    counterexample[name] = 0
                else:
                    counterexample[name] = value.as_long()

            return False, counterexample

        raise RuntimeError("Z3 returned unknown.")
