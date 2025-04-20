#!/usr/bin/env python3
import typer
from cli.analyze import analyze
from cli.verify import verify
from cli.test import test

app = typer.Typer(help="Spectorin: AI‑powered formal verification & testing")

app.add_typer(analyze,   name="analyze",  help="Static analysis")
app.add_typer(verify,    name="verify",   help="Formal verification")
app.add_typer(test,      name="test",     help="Dynamic testing / fuzzing")

if __name__ == "__main__":
    app()
