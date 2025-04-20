# core/parsers/python_ast_parser.py
from core.parsers.tree_sitter_loader import get_parser
import json

def parse_python(code: str):
    parser = get_parser("python")
    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node
    return root_node
