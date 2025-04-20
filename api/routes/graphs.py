# api/routes/graphs.py
from fastapi import APIRouter, Request
from core.parsers.python_ast_parser import parse_python
from core.graphs.cfg_generator import build_cfg_from_ast, export_cfg_json

router = APIRouter()

@router.post("/cfg")
async def get_cfg(request: Request):
    data = await request.json()
    code = data.get("code")

    ast = parse_python(code)
    cfg = build_cfg_from_ast(ast)
    return export_cfg_json(cfg)
