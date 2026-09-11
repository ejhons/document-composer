from dcp_application.composition import create_build_document
import typer
from pathlib import Path
from dcp_cli.interaction.terminal import TerminalInteraction
from dcp_engine.runtime.engine import IteractionResult
from dcp_cli.interaction.prompts import resolve_pending


# def build(
#     root: Path = typer.Argument(...),
#     target_format: str = typer.Option("default"),
# ):
def build(
    root: Path = typer.Argument(
        Path('.'),
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        help="Path to the project workspace. Defaults to the current directory.",
    ),
    target_format: str = typer.Option(
        "default",
        "--format",
        "-f",
        help="Target document format.",
    ),
) -> None:
    # Usa caminho absoluto para o root
    root = root.resolve()
    #Creates a Engine object with default properties.
    # engine = EngineBuilder.default().build()
    # BuildDocument(engine)
    use_case = create_build_document(
        TerminalInteraction.default()
    ) 

    values = {}
    """Inicia uma nova sessão."""
    session = use_case.start(root)
    typer.secho("Sessão iniciada.", fg=typer.colors.BLUE)

    """Abre ou processa os formulários da sessão."""
    typer.echo("Carregando formulários da sessão...")
    while True:
        interaction:IteractionResult = use_case.interact(
            session=session,
            values=values,
        )

        if interaction.is_solved:
            break
        # Estabilish iteration with user and save results as a dict[key, user_value]
        values = resolve_pending(
            pending=interaction.pending,
            iteration_port=use_case.interaction
        )

    typer.echo("Compilando documento...")
    result = use_case.compile(
        session=session,
        target_format=target_format,
    )

    """Encerra a sessão atual."""
    typer.secho("Sessão encerrada.", fg=typer.colors.RED)

    typer.echo(f"Output: {result.output_compiled}")