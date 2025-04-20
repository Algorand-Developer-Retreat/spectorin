import typer
from rich import print
from core.engine import Engine

analyze = typer.Typer()

@analyze.command()
def run(
    path: str = typer.Argument(..., help="Path to code or contract"),
    chain: str = typer.Option("solidity", help="Blockchain or language plugin")
):
    """
    Run static analysis on the given file or directory.
    """
    print(f"[bold green]🔍 Running static analysis on[/] {path} (plugin={chain})")
    engine = Engine()
    results = engine.static_analyze(path, plugin=chain)
    print(results)
