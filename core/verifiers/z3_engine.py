# core/verifiers/z3_engine.py
from z3 import Solver
from core.parsers.python_ast_parser import parse_python
from core.verifiers.ast_to_z3 import ast_to_constraints

class Z3Verifier:
    def verify(self, code: str, properties=None):
        ast = parse_python(code)
        constraints, variables = ast_to_constraints(ast)

        s = Solver()
        for c in constraints:
            s.add(c)

        result = {
            "status": "pass" if s.check() == unsat else "fail",
            "model": str(s.model()) if s.check() == sat else None,
        }
        return result
