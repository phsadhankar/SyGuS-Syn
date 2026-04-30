from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Set


SExpr = Any


@dataclass
class SyGuSBenchmark:
    logic: str = "LIA"
    synth_name: str = ""
    synth_args: List[str] = field(default_factory=list)
    declared_vars: List[str] = field(default_factory=list)
    constraints: List[SExpr] = field(default_factory=list)
    constants: List[int] = field(default_factory=lambda: [0, 1])
    int_ops: Set[str] = field(default_factory=set)
    bool_ops: Set[str] = field(default_factory=set)

    @property
    def variable_names(self) -> List[str]:
        return self.synth_args or self.declared_vars


def tokenize(text: str) -> List[str]:
    clean_lines = []
    for line in text.splitlines():
        if ";" in line:
            line = line[: line.index(";")]
        clean_lines.append(line)

    text = "\n".join(clean_lines)
    text = text.replace("(", " ( ").replace(")", " ) ")
    return text.split()


def parse_tokens(tokens: List[str]) -> List[SExpr]:
    def parse_one(index: int):
        if tokens[index] == "(":
            result = []
            index += 1

            while index < len(tokens) and tokens[index] != ")":
                child, index = parse_one(index)
                result.append(child)

            if index >= len(tokens):
                raise ValueError("Unbalanced parentheses in SyGuS file.")

            return result, index + 1

        if tokens[index] == ")":
            raise ValueError("Unexpected ')' in SyGuS file.")

        atom = tokens[index]

        try:
            return int(atom), index + 1
        except ValueError:
            return atom, index + 1

    commands = []
    index = 0

    while index < len(tokens):
        expr, index = parse_one(index)
        commands.append(expr)

    return commands


def parse_file(path: str) -> SyGuSBenchmark:
    with open(path, "r", encoding="utf-8") as file:
        return parse_text(file.read())


def parse_text(text: str) -> SyGuSBenchmark:
    commands = parse_tokens(tokenize(text))
    bench = SyGuSBenchmark()

    for cmd in commands:
        if not isinstance(cmd, list) or not cmd:
            continue

        head = cmd[0]

        if head == "set-logic" and len(cmd) >= 2:
            bench.logic = str(cmd[1])

        elif head == "declare-var" and len(cmd) >= 3:
            if cmd[2] != "Int":
                raise ValueError("This minimal solver only supports Int variables.")
            bench.declared_vars.append(str(cmd[1]))

        elif head == "synth-fun":
            parse_synth_fun(cmd, bench)

        elif head == "constraint" and len(cmd) == 2:
            bench.constraints.append(cmd[1])

    if not bench.synth_name:
        raise ValueError("No synth-fun command found.")

    if not bench.constraints:
        raise ValueError("No constraints found.")

    if not bench.constants:
        bench.constants = [0, 1]

    if not bench.int_ops:
        bench.int_ops = {"+", "-", "ite"}

    if not bench.bool_ops:
        bench.bool_ops = {">=", "<=", "=", ">", "<"}

    return bench


def parse_synth_fun(cmd: List[SExpr], bench: SyGuSBenchmark) -> None:
    bench.synth_name = str(cmd[1])

    args = cmd[2]
    if not isinstance(args, list):
        raise ValueError("Unsupported synth-fun argument list.")

    bench.synth_args = []

    for arg in args:
        if isinstance(arg, list) and len(arg) >= 2:
            if arg[1] != "Int":
                raise ValueError("This minimal solver only supports Int synth-fun arguments.")
            bench.synth_args.append(str(arg[0]))

    return_type = cmd[3]

    if return_type != "Int":
        raise ValueError("This minimal solver only synthesizes Int-returning functions.")

    if len(cmd) >= 5 and isinstance(cmd[4], list):
        extract_grammar(cmd[4], bench)


def extract_grammar(grammar: List[SExpr], bench: SyGuSBenchmark) -> None:
    int_ops: Set[str] = set()
    bool_ops: Set[str] = set()
    constants: Set[int] = set()

    def visit(prod: SExpr):
        if isinstance(prod, int):
            constants.add(prod)
            return

        if isinstance(prod, str):
            return

        if not isinstance(prod, list) or not prod:
            return

        op = prod[0]

        if op in {"+", "-", "ite"}:
            int_ops.add(op)

        elif op in {">=", "<=", ">", "<", "="}:
            bool_ops.add(op)

        elif op in {"and", "or", "not", "=>"}:
            bool_ops.add(op)

        for item in prod[1:]:
            visit(item)

    for nonterminal in grammar:
        if not isinstance(nonterminal, list) or len(nonterminal) < 3:
            continue

        productions = nonterminal[2]

        if not isinstance(productions, list):
            continue

        for prod in productions:
            visit(prod)

    bench.constants = sorted(constants) if constants else [0, 1]
    bench.int_ops = int_ops if int_ops else {"+", "-", "ite"}
    bench.bool_ops = bool_ops if bool_ops else {">=", "<=", "=", ">", "<"}
