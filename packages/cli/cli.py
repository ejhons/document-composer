import typer

from doc_composer_cli.commands.build import build


app = typer.Typer(
    name="composer",
    help="Document Composer command-line interface.",
    no_args_is_help=True,
)

app.command()(build)