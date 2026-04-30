from __future__ import annotations

from typing import Any, Dict
import z3

from ast_nodes import Expr
from sygus_parser import SyGuSBenchmark, SExpr


def spec_holds_on_example(
    bench: SyGuSBenchmark,
    candidate: Expr,
    env: Dict[str, int],
) -> bool:
    return all(bool(eval_constraint(c, bench, candidate, env)) for c in bench.constraints)


def eval_constraint(
    node: SExpr,
    bench: SyGuSBenchmark,
    candidate: Expr,
    env: Dict[str, int],
) -> Any:
    if isinstance(node, int):
        return node

    if isinstance(node, str):
        if node == "true":
            return True

        if node == "false":
            return False

        return env[node]

    op = node[0]
    args = node[1:]

    if op == bench.synth_name:
        local_env = dict(env)

        for param, actual in zip(bench.synth_args, args):
            local_env[param] = int(eval_constraint(actual, bench, candidate, env))

        return candidate.eval(local_env)

    if op == "+":
        return sum(int(eval_constraint(a, bench, candidate, env)) for a in args)

    if op == "-":
        if len(args) == 1:
            return -int(eval_constraint(args[0], bench, candidate, env))

        value = int(eval_constraint(args[0], bench, candidate, env))

        for arg in args[1:]:
            value -= int(eval_constraint(arg, bench, candidate, env))

        return value

    if op == "ite":
        condition = bool(eval_constraint(args[0], bench, candidate, env))

        if condition:
            return eval_constraint(args[1], bench, candidate, env)

        return eval_constraint(args[2], bench, candidate, env)

    if op == "=":
        return eval_constraint(args[0], bench, candidate, env) == eval_constraint(args[1], bench, candidate, env)

    if op == ">=":
        return int(eval_constraint(args[0], bench, candidate, env)) >= int(eval_constraint(args[1], bench, candidate, env))

    if op == "<=":
        return int(eval_constraint(args[0], bench, candidate, env)) <= int(eval_constraint(args[1], bench, candidate, env))

    if op == ">":
        return int(eval_constraint(args[0], bench, candidate, env)) > int(eval_constraint(args[1], bench, candidate, env))

    if op == "<":
        return int(eval_constraint(args[0], bench, candidate, env)) < int(eval_constraint(args[1], bench, candidate, env))

    if op == "and":
        return all(bool(eval_constraint(a, bench, candidate, env)) for a in args)

    if op == "or":
        return any(bool(eval_constraint(a, bench, candidate, env)) for a in args)

    if op == "not":
        return not bool(eval_constraint(args[0], bench, candidate, env))

    if op == "=>":
        left = bool(eval_constraint(args[0], bench, candidate, env))
        right = bool(eval_constraint(args[1], bench, candidate, env))
        return (not left) or right

    raise ValueError(f"Unsupported operator in constraint evaluation: {op}")


def constraint_to_z3(
    node: SExpr,
    bench: SyGuSBenchmark,
    candidate: Expr,
    z3_vars: Dict[str, z3.IntNumRef],
) -> Any:
    if isinstance(node, int):
        return z3.IntVal(node)

    if isinstance(node, str):
        if node == "true":
            return z3.BoolVal(True)

        if node == "false":
            return z3.BoolVal(False)

        return z3_vars[node]

    op = node[0]
    args = node[1:]

    if op == bench.synth_name:
        local_vars = dict(z3_vars)

        for param, actual in zip(bench.synth_args, args):
            local_vars[param] = constraint_to_z3(actual, bench, candidate, z3_vars)

        return candidate.to_z3(local_vars)

    zargs = [constraint_to_z3(a, bench, candidate, z3_vars) for a in args]

    if op == "+":
        total = z3.IntVal(0)

        for a in zargs:
            total = total + a

        return total

    if op == "-":
        if len(zargs) == 1:
            return -zargs[0]

        result = zargs[0]

        for a in zargs[1:]:
            result = result - a

        return result

    if op == "ite":
        return z3.If(zargs[0], zargs[1], zargs[2])

    if op == "=":
        return zargs[0] == zargs[1]

    if op == ">=":
        return zargs[0] >= zargs[1]

    if op == "<=":
        return zargs[0] <= zargs[1]

    if op == ">":
        return zargs[0] > zargs[1]

    if op == "<":
        return zargs[0] < zargs[1]

    if op == "and":
        return z3.And(*zargs)

    if op == "or":
        return z3.Or(*zargs)

    if op == "not":
        return z3.Not(zargs[0])

    if op == "=>":
        return z3.Implies(zargs[0], zargs[1])

    raise ValueError(f"Unsupported operator in Z3 conversion: {op}")
