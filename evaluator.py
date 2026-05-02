from typing import Dict, List

from ast_nodes import Expr
from spec import spec_holds_on_example
from sygus_parser import SyGuSBenchmark


def candidate_passes_examples(
    candidate: Expr,
    bench: SyGuSBenchmark,
    examples: List[Dict[str, int]],
) -> bool:
    for env in examples:
        if not spec_holds_on_example(bench, candidate, env):
            return False

    return True
