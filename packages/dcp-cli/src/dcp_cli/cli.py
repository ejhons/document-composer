from __future__ import annotations

import typer
from importlib.metadata import version

from dcp_cli.commands.build import build

__version__ = version("dcp-cli")

def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"Doc Composer CLI {__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="dcp",
    help="Document Composer command-line interface.",
    no_args_is_help=True,
)


app.command()(build)

@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the installed version and exit.",
    ),
) -> None:
    pass