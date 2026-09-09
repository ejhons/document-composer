from pathlib import Path

import typer

from doc_composer_cli.presentation.prompts import resolve_pending


def build(
    recipe: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Path to the recipe manifest.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory.",
    ),
):
    """
    Build a document from a recipe manifest.
    """

    from doc_engine.application.build import BuildDocumentUseCase

    use_case = BuildDocumentUseCase()

    session = use_case.create_session(
        recipe_path=recipe,
        output_path=output,
    )

    while True:
        result = use_case.execute(session)

        if result.is_success:
            typer.echo()
            typer.secho(
                "Document successfully built.",
                fg=typer.colors.GREEN,
                bold=True,
            )

            typer.echo(f"Output: {result.output_path}")
            break

        if result.is_pending:
            resolve_pending(
                result.pending,
                session.context,
            )
            continue

        typer.secho(
            result.message or "Document build failed.",
            fg=typer.colors.RED,
            err=True,
        )

        raise typer.Exit(code=1)