from typing import Dict, List, Set
from ast_nodes import Expr, Var, Const, Add, Sub, Ite, Ge, Le


class BottomUpEnumerator:
    def __init__(self, variable_names=None, constants=None, max_size=7):
        self.variable_names = variable_names or ["x", "y"]
        self.constants = constants or [0, 1]
        self.max_size = max_size
        self.generated_count = 0
        self.seen: Set[str] = set()

    def enumerate(self):
        expressions_by_size: Dict[int, List[Expr]] = {}

        base_exprs: List[Expr] = []

        for var in self.variable_names:
            base_exprs.append(Var(var))

        for const in self.constants:
            base_exprs.append(Const(const))

        expressions_by_size[1] = []

        for expr in base_exprs:
            if str(expr) not in self.seen:
                self.seen.add(str(expr))
                expressions_by_size[1].append(expr)
                self.generated_count += 1
                yield expr

        for size in range(2, self.max_size + 1):
            current_level: List[Expr] = []

            for left_size in range(1, size):
                right_size = size - 1 - left_size

                if left_size not in expressions_by_size or right_size not in expressions_by_size:
                    continue

                for left in expressions_by_size[left_size]:
                    for right in expressions_by_size[right_size]:
                        candidates = [
                            Add(left, right),
                            Sub(left, right),
                        ]

                        for candidate in candidates:
                            key = str(candidate)
                            if key not in self.seen:
                                self.seen.add(key)
                                current_level.append(candidate)
                                self.generated_count += 1
                                yield candidate

            for cond_size in range(1, size):
                for then_size in range(1, size):
                    else_size = size - 1 - cond_size - then_size

                    if else_size < 1:
                        continue

                    if then_size not in expressions_by_size or else_size not in expressions_by_size:
                        continue

                    all_exprs_for_conditions = []
                    for level_exprs in expressions_by_size.values():
                        all_exprs_for_conditions.extend(level_exprs)

                    for a in all_exprs_for_conditions:
                        for b in all_exprs_for_conditions:
                            conditions = [
                                Ge(a, b),
                                Le(a, b),
                            ]

                            for condition in conditions:
                                if condition.size() != cond_size:
                                    continue

                                for then_expr in expressions_by_size[then_size]:
                                    for else_expr in expressions_by_size[else_size]:
                                        candidate = Ite(condition, then_expr, else_expr)
                                        key = str(candidate)

                                        if key not in self.seen:
                                            self.seen.add(key)
                                            current_level.append(candidate)
                                            self.generated_count += 1
                                            yield candidate

            expressions_by_size[size] = current_level
