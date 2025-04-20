# core/parsers/tree_sitter_loader.py
from tree_sitter import Language, Parser
import os

TREE_SITTER_LANG_PATH = "core/parsers/tree_sitter_lang.so"

Language.build_library(
    # Output shared library
    TREE_SITTER_LANG_PATH,
    # List of languages
    [
        "vendor/tree-sitter-python",
        "vendor/tree-sitter-solidity",
        "vendor/tree-sitter-rust"
    ]
)

PY_LANGUAGE = Language(TREE_SITTER_LANG_PATH, "python")

def get_parser(language: str):
    parser = Parser()
    lang_map = {
        "python": PY_LANGUAGE,
        # Add others here
    }
    parser.set_language(lang_map[language])
    return parser
