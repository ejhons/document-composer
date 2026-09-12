from dataclasses import dataclass
from typing import Annotated
from pprint import pprint
import typer
from pathlib import Path

from dcp_cli.interaction.terminal import TerminalInteraction
from dcp_cli.interaction.prompts import resolve_pending
from dcp_application.composition import create_build_document

from dcp_engine import IteractionResult, logger, setup_logger

# setup_logger()

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
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Activate detailed mode.")
) -> None:
    try:
        if verbose:
            setup_logger()
        
        # Usa caminho absoluto para o root
        root = root.resolve()
        #Creates a Engine object with default properties.
        use_case = create_build_document(
            TerminalInteraction.default()
        ) 

        values = {}
        """Inicia uma nova sessão."""
        session = use_case.start(root)
        typer.secho("Session started.", fg=typer.colors.GREEN)

        """Abre ou processa os formulários da sessão."""
        typer.echo("Loading session forms...")
        while True:
            interaction:IteractionResult = use_case.interact(
                session=session,
                values=values,
            )
            # pprint(interaction.pending.model_dump_json())

            if interaction.is_solved:
                break
            # Estabilish iteraction with user and save results as a dict[key, user_value]
            values = resolve_pending(
                pending=interaction.pending,
                iteraction_port=use_case.interaction
            )

        typer.echo("Compiling document...")
        result = use_case.compile(
            session=session,
            target_format=target_format,
        )

        """Encerra a sessão atual."""
        typer.echo(f"Output: {result.output_compiled}")
        typer.secho("Session closed.", fg=typer.colors.GREEN)

        return BuildResult(
            code=0,
            msg="Build complete successfully",
            output_path=result.output_compiled
        )
    except Exception as e:
        return BuildResult(
            code=1,
            msg=str(e)
        )


@dataclass(frozen=True)
class BuildResult:
    code: int
    msg: str
    output_path: Path | None = None