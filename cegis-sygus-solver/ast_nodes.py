from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set
import z3


class Expr:
    def eval(self, env: Dict[str, int]) -> int:
        raise NotImplementedError

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.ArithRef:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError

    def vars(self) -> Set[str]:
        raise NotImplementedError


class BoolExpr:
    def eval(self, env: Dict[str, int]) -> bool:
        raise NotImplementedError

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.BoolRef:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True)
class Var(Expr):
    name: str

    def eval(self, env):
        return int(env[self.name])

    def to_z3(self, z3_vars):
        return z3_vars[self.name]

    def size(self):
        return 1

    def vars(self):
        return {self.name}

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Const(Expr):
    value: int

    def eval(self, env):
        return self.value

    def to_z3(self, z3_vars):
        return z3.IntVal(self.value)

    def size(self):
        return 1

    def vars(self):
        return set()

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class Add(Expr):
    left: Expr
    right: Expr

    def eval(self, env):
        return self.left.eval(env) + self.right.eval(env)

    def to_z3(self, z3_vars):
        return self.left.to_z3(z3_vars) + self.right.to_z3(z3_vars)

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def vars(self):
        return self.left.vars() | self.right.vars()

    def __str__(self):
        return f"(+ {self.left} {self.right})"


@dataclass(frozen=True)
class Sub(Expr):
    left: Expr
    right: Expr

    def eval(self, env):
        return self.left.eval(env) - self.right.eval(env)

    def to_z3(self, z3_vars):
        return self.left.to_z3(z3_vars) - self.right.to_z3(z3_vars)

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def vars(self):
        return self.left.vars() | self.right.vars()

    def __str__(self):
        return f"(- {self.left} {self.right})"


@dataclass(frozen=True)
class Neg(Expr):
    expr: Expr

    def eval(self, env):
        return -self.expr.eval(env)

    def to_z3(self, z3_vars):
        return -self.expr.to_z3(z3_vars)

    def size(self):
        return 1 + self.expr.size()

    def vars(self):
        return self.expr.vars()

    def __str__(self):
        return f"(- {self.expr})"


@dataclass(frozen=True)
class Mul(Expr):
    left: Expr
    right: Expr

    def eval(self, env):
        return self.left.eval(env) * self.right.eval(env)

    def to_z3(self, z3_vars):
        return self.left.to_z3(z3_vars) * self.right.to_z3(z3_vars)

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def vars(self):
        return self.left.vars() | self.right.vars()

    def __str__(self):
        return f"(* {self.left} {self.right})"


@dataclass(frozen=True)
class Ite(Expr):
    condition: BoolExpr
    then_expr: Expr
    else_expr: Expr

    def eval(self, env):
        return self.then_expr.eval(env) if self.condition.eval(env) else self.else_expr.eval(env)

    def to_z3(self, z3_vars):
        return z3.If(
            self.condition.to_z3(z3_vars),
            self.then_expr.to_z3(z3_vars),
            self.else_expr.to_z3(z3_vars),
        )

    def size(self):
        return 1 + self.condition.size() + self.then_expr.size() + self.else_expr.size()

    def vars(self):
        return self.then_expr.vars() | self.else_expr.vars()

    def __str__(self):
        return f"(ite {self.condition} {self.then_expr} {self.else_expr})"


@dataclass(frozen=True)
class Eq(BoolExpr):
    left: Expr
    right: Expr

    def eval(self, env):
        return self.left.eval(env) == self.right.eval(env)

    def to_z3(self, z3_vars):
        return self.left.to_z3(z3_vars) == self.right.to_z3(z3_vars)

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def __str__(self):
        return f"(= {self.left} {self.right})"


@dataclass(frozen=True)
class Ge(BoolExpr):
    left: Expr
    right: Expr

    def eval(self, env):
        return self.left.eval(env) >= self.right.eval(env)

    def to_z3(self, z3_vars):
        return self.left.to_z3(z3_vars) >= self.right.to_z3(z3_vars)

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def __str__(self):
        return f"(>= {self.left} {self.right})"


@dataclass(frozen=True)
class Le(BoolExpr):
    left: Expr
    right: Expr

    def eval(self, env):
        return self.left.eval(env) <= self.right.eval(env)

    def to_z3(self, z3_vars):
        return self.left.to_z3(z3_vars) <= self.right.to_z3(z3_vars)

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def __str__(self):
        return f"(<= {self.left} {self.right})"


@dataclass(frozen=True)
class Gt(BoolExpr):
    left: Expr
    right: Expr

    def eval(self, env):
        return self.left.eval(env) > self.right.eval(env)

    def to_z3(self, z3_vars):
        return self.left.to_z3(z3_vars) > self.right.to_z3(z3_vars)

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def __str__(self):
        return f"(> {self.left} {self.right})"


@dataclass(frozen=True)
class Lt(BoolExpr):
    left: Expr
    right: Expr

    def eval(self, env):
        return self.left.eval(env) < self.right.eval(env)

    def to_z3(self, z3_vars):
        return self.left.to_z3(z3_vars) < self.right.to_z3(z3_vars)

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def __str__(self):
        return f"(< {self.left} {self.right})"


@dataclass(frozen=True)
class And(BoolExpr):
    left: BoolExpr
    right: BoolExpr

    def eval(self, env):
        return self.left.eval(env) and self.right.eval(env)

    def to_z3(self, z3_vars):
        return z3.And(self.left.to_z3(z3_vars), self.right.to_z3(z3_vars))

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def __str__(self):
        return f"(and {self.left} {self.right})"


@dataclass(frozen=True)
class Or(BoolExpr):
    left: BoolExpr
    right: BoolExpr

    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)

    def to_z3(self, z3_vars):
        return z3.Or(self.left.to_z3(z3_vars), self.right.to_z3(z3_vars))

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def __str__(self):
        return f"(or {self.left} {self.right})"


@dataclass(frozen=True)
class Not(BoolExpr):
    expr: BoolExpr

    def eval(self, env):
        return not self.expr.eval(env)

    def to_z3(self, z3_vars):
        return z3.Not(self.expr.to_z3(z3_vars))

    def size(self):
        return 1 + self.expr.size()

    def __str__(self):
        return f"(not {self.expr})"


@dataclass(frozen=True)
class Implies(BoolExpr):
    left: BoolExpr
    right: BoolExpr

    def eval(self, env):
        return (not self.left.eval(env)) or self.right.eval(env)

    def to_z3(self, z3_vars):
        return z3.Implies(self.left.to_z3(z3_vars), self.right.to_z3(z3_vars))

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def __str__(self):
        return f"(=> {self.left} {self.right})"