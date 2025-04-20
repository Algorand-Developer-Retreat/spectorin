import typer
from rich import print
from core.engine import Engine

verify = typer.Typer()

@verify.command()
def run(
    path: str = typer.Argument(..., help="Path to source file"),
    property: str = typer.Option(..., "--property", "-p", help="Property to verify")
):
    """
    Perform formal verification on the given source.
    """
    print(f"[bold blue]🔒 Verifying[/] {path} [italic]{property}[/]")
    engine = Engine()
    proof = engine.formal_verify(path, property)
    print(proof)
