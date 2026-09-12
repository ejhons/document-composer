from __future__ import annotations

import typer

from dcp_cli.commands.build import build

app = typer.Typer(
    name="dcp",
    help="Document Composer command-line interface.",
    no_args_is_help=True,
)


app.command()(build)