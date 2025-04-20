# core/verifiers/ast_to_z3.py
from z3 import *

def ast_to_constraints(ast):
    constraints = []
    variables = {}

    def walk(node):
        if node.type == 'assignment':
            var_name = node.child_by_field_name('left').text.decode()
            value_node = node.child_by_field_name('right')
            if value_node.type == 'integer':
                value = int(value_node.text.decode())
                variables[var_name] = Int(var_name)
                constraints.append(variables[var_name] == value)

        elif node.type == 'assert_statement':
            condition = node.child_by_field_name('condition')
            if condition.type == 'binary_operator':
                left = condition.child_by_field_name('left').text.decode()
                right = int(condition.child_by_field_name('right').text.decode())
                operator = condition.child_by_field_name('operator').text.decode()
                if left in variables:
                    if operator == '>':
                        constraints.append(variables[left] > right)
                    elif operator == '<':
                        constraints.append(variables[left] < right)
                    elif operator == '==':
                        constraints.append(variables[left] == right)

        # Recursively walk children
        for child in node.children:
            walk(child)

    walk(ast)
    return constraints, variables
