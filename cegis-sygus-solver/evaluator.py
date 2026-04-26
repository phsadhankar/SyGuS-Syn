from typing import Dict, List
from ast_nodes import Expr


def candidate_passes_examples(candidate: Expr, examples: List[Dict[str, int]], spec_func) -> bool:
    for env in examples:
        output = candidate.eval(env)
        if not spec_func(env, output):
            return False
    return True
