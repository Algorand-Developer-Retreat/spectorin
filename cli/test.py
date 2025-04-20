import typer
from rich import print
from core.engine import Engine

test = typer.Typer()

@test.command()
def run(
    path: str = typer.Argument(..., help="Path to code or contract"),
    max_runs: int = typer.Option(100, "--max-runs", "-n", help="Maximum fuzz iterations")
):
    """
    Run dynamic testing / fuzzing on the given code.
    """
    print(f"[bold magenta]🎯 Fuzz testing[/] {path} for {max_runs} runs")
    engine = Engine()
    report = engine.fuzz_test(path, max_runs)
    print(report)
