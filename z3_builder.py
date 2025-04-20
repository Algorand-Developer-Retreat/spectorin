from z3 import *

class Z3ConstraintBuilder:
    def __init__(self):
        self.solver = Solver()
        self.variables = {}

    def build_constraints(self, ir_blocks):
        for block in ir_blocks:
            for stmt in block.get("statements", []):
                self._translate_statement(stmt)

    def _translate_statement(self, stmt):
        kind = stmt.get("type")
        if kind == "assignment":
            var = stmt["target"]
            expr = stmt["expression"]
            z3_expr = self._eval_expr(expr)
            self._assign(var, z3_expr)
        elif kind in {"assert", "require"}:
            expr = stmt["expression"]
            z3_expr = self._eval_expr(expr)
            self.solver.add(z3_expr)

    def _assign(self, var_name, expr):
        if var_name not in self.variables:
            self.variables[var_name] = Int(var_name)
        self.solver.add(self.variables[var_name] == expr)

    def _eval_expr(self, expr):
        if expr["type"] == "literal":
            return IntVal(int(expr["value"]))
        elif expr["type"] == "identifier":
            name = expr["name"]
            if name not in self.variables:
                self.variables[name] = Int(name)
            return self.variables[name]
        elif expr["type"] == "binary":
            op = expr["operator"]
            left = self._eval_expr(expr["left"])
            right = self._eval_expr(expr["right"])
            return self._apply_binary_operator(op, left, right)
        raise ValueError(f"Unknown expression type: {expr['type']}")

    def _apply_binary_operator(self, op, left, right):
        return {
            "+": left + right,
            "-": left - right,
            "*": left * right,
            "/": left / right,
            "==": left == right,
            "!=": left != right,
            "<": left < right,
            "<=": left <= right,
            ">": left > right,
            ">=": left >= right
        }.get(op, None)

    def check(self):
        return self.solver.check()

    def model(self):
        if self.solver.check() == sat:
            return self.solver.model()
        return None
