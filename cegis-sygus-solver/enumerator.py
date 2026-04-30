from __future__ import annotations

from typing import Dict, Iterable, List, Set

from ast_nodes import Add, Const, Eq, Expr, Ge, Gt, Ite, Le, Lt, Sub, Var, BoolExpr


class BottomUpEnumerator:
    def __init__(
        self,
        variable_names: List[str],
        constants: List[int],
        int_ops: Set[str],
        bool_ops: Set[str],
        max_size: int = 9,
    ):
        self.variable_names = variable_names
        self.constants = constants
        self.int_ops = int_ops
        self.bool_ops = bool_ops
        self.max_size = max_size

        self.generated_count = 0
        self.seen_exprs: Set[str] = set()
        self.seen_bools: Set[str] = set()

    def enumerate(self) -> Iterable[Expr]:
        exprs_by_size: Dict[int, List[Expr]] = {
            i: [] for i in range(1, self.max_size + 1)
        }

        bools_by_size: Dict[int, List[BoolExpr]] = {
            i: [] for i in range(1, self.max_size + 1)
        }

        base_exprs: List[Expr] = []

        for variable in self.variable_names:
            base_exprs.append(Var(variable))

        for constant in self.constants:
            base_exprs.append(Const(constant))

        for expr in base_exprs:
            if self._add_expr(expr, exprs_by_size[1]):
                yield expr

        for size in range(2, self.max_size + 1):
            self._build_bools_of_size(size, exprs_by_size, bools_by_size)

            for left_size in range(1, size):
                right_size = size - 1 - left_size

                if right_size < 1:
                    continue

                for left in exprs_by_size.get(left_size, []):
                    for right in exprs_by_size.get(right_size, []):
                        if "+" in self.int_ops:
                            candidate = Add(left, right)

                            if self._add_expr(candidate, exprs_by_size[size]):
                                yield candidate

                        if "-" in self.int_ops:
                            candidate = Sub(left, right)

                            if self._add_expr(candidate, exprs_by_size[size]):
                                yield candidate

            if "ite" in self.int_ops:
                for cond_size in range(1, size):
                    for then_size in range(1, size):
                        else_size = size - 1 - cond_size - then_size

                        if else_size < 1:
                            continue

                        for condition in bools_by_size.get(cond_size, []):
                            for then_expr in exprs_by_size.get(then_size, []):
                                for else_expr in exprs_by_size.get(else_size, []):
                                    candidate = Ite(condition, then_expr, else_expr)

                                    if self._add_expr(candidate, exprs_by_size[size]):
                                        yield candidate

    def _build_bools_of_size(
        self,
        size: int,
        exprs_by_size: Dict[int, List[Expr]],
        bools_by_size: Dict[int, List[BoolExpr]],
    ) -> None:
        for left_size in range(1, size):
            right_size = size - 1 - left_size

            if right_size < 1:
                continue

            for left in exprs_by_size.get(left_size, []):
                for right in exprs_by_size.get(right_size, []):
                    candidates: List[BoolExpr] = []

                    if ">=" in self.bool_ops:
                        candidates.append(Ge(left, right))

                    if "<=" in self.bool_ops:
                        candidates.append(Le(left, right))

                    if ">" in self.bool_ops:
                        candidates.append(Gt(left, right))

                    if "<" in self.bool_ops:
                        candidates.append(Lt(left, right))

                    if "=" in self.bool_ops:
                        candidates.append(Eq(left, right))

                    for candidate in candidates:
                        self._add_bool(candidate, bools_by_size[size])

    def _add_expr(self, expr: Expr, bucket: List[Expr]) -> bool:
        key = str(expr)

        if key in self.seen_exprs:
            return False

        self.seen_exprs.add(key)
        bucket.append(expr)
        self.generated_count += 1

        return True

    def _add_bool(self, expr: BoolExpr, bucket: List[BoolExpr]) -> bool:
        key = str(expr)

        if key in self.seen_bools:
            return False

        self.seen_bools.add(key)
        bucket.append(expr)

        return True
