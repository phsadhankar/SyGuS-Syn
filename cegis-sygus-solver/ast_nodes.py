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


@dataclass(frozen=True)
class Var(Expr):
    name: str

    def eval(self, env: Dict[str, int]) -> int:
        return env[self.name]

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.ArithRef:
        return z3_vars[self.name]

    def size(self) -> int:
        return 1

    def vars(self) -> Set[str]:
        return {self.name}

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Const(Expr):
    value: int

    def eval(self, env: Dict[str, int]) -> int:
        return self.value

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.ArithRef:
        return z3.IntVal(self.value)

    def size(self) -> int:
        return 1

    def vars(self) -> Set[str]:
        return set()

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Add(Expr):
    left: Expr
    right: Expr

    def eval(self, env: Dict[str, int]) -> int:
        return self.left.eval(env) + self.right.eval(env)

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.ArithRef:
        return self.left.to_z3(z3_vars) + self.right.to_z3(z3_vars)

    def size(self) -> int:
        return 1 + self.left.size() + self.right.size()

    def vars(self) -> Set[str]:
        return self.left.vars() | self.right.vars()

    def __str__(self) -> str:
        return f"(+ {self.left} {self.right})"


@dataclass(frozen=True)
class Sub(Expr):
    left: Expr
    right: Expr

    def eval(self, env: Dict[str, int]) -> int:
        return self.left.eval(env) - self.right.eval(env)

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.ArithRef:
        return self.left.to_z3(z3_vars) - self.right.to_z3(z3_vars)

    def size(self) -> int:
        return 1 + self.left.size() + self.right.size()

    def vars(self) -> Set[str]:
        return self.left.vars() | self.right.vars()

    def __str__(self) -> str:
        return f"(- {self.left} {self.right})"


class BoolExpr:
    def eval(self, env: Dict[str, int]) -> bool:
        raise NotImplementedError

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.BoolRef:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True)
class Ge(BoolExpr):
    left: Expr
    right: Expr

    def eval(self, env: Dict[str, int]) -> bool:
        return self.left.eval(env) >= self.right.eval(env)

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.BoolRef:
        return self.left.to_z3(z3_vars) >= self.right.to_z3(z3_vars)

    def size(self) -> int:
        return 1 + self.left.size() + self.right.size()

    def __str__(self) -> str:
        return f"(>= {self.left} {self.right})"


@dataclass(frozen=True)
class Le(BoolExpr):
    left: Expr
    right: Expr

    def eval(self, env: Dict[str, int]) -> bool:
        return self.left.eval(env) <= self.right.eval(env)

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.BoolRef:
        return self.left.to_z3(z3_vars) <= self.right.to_z3(z3_vars)

    def size(self) -> int:
        return 1 + self.left.size() + self.right.size()

    def __str__(self) -> str:
        return f"(<= {self.left} {self.right})"


@dataclass(frozen=True)
class Eq(BoolExpr):
    left: Expr
    right: Expr

    def eval(self, env: Dict[str, int]) -> bool:
        return self.left.eval(env) == self.right.eval(env)

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.BoolRef:
        return self.left.to_z3(z3_vars) == self.right.to_z3(z3_vars)

    def size(self) -> int:
        return 1 + self.left.size() + self.right.size()

    def __str__(self) -> str:
        return f"(= {self.left} {self.right})"


@dataclass(frozen=True)
class Or(BoolExpr):
    left: BoolExpr
    right: BoolExpr

    def eval(self, env: Dict[str, int]) -> bool:
        return self.left.eval(env) or self.right.eval(env)

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.BoolRef:
        return z3.Or(self.left.to_z3(z3_vars), self.right.to_z3(z3_vars))

    def size(self) -> int:
        return 1 + self.left.size() + self.right.size()

    def __str__(self) -> str:
        return f"(or {self.left} {self.right})"


@dataclass(frozen=True)
class Ite(Expr):
    condition: BoolExpr
    then_expr: Expr
    else_expr: Expr

    def eval(self, env: Dict[str, int]) -> int:
        if self.condition.eval(env):
            return self.then_expr.eval(env)
        return self.else_expr.eval(env)

    def to_z3(self, z3_vars: Dict[str, z3.Int]) -> z3.ArithRef:
        return z3.If(
            self.condition.to_z3(z3_vars),
            self.then_expr.to_z3(z3_vars),
            self.else_expr.to_z3(z3_vars),
        )

    def size(self) -> int:
        return 1 + self.condition.size() + self.then_expr.size() + self.else_expr.size()

    def vars(self) -> Set[str]:
        return self.then_expr.vars() | self.else_expr.vars()

    def __str__(self) -> str:
        return f"(ite {self.condition} {self.then_expr} {self.else_expr})"
