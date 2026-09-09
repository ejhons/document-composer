import typer
from typing import Iterable
from dcp_api.domain.iteraction import PendingResolution



def resolve_pending(
    pending: Iterable[PendingResolution],
    context,
) -> None:

    for request in pending:

        value = typer.prompt(
            request.name,
            default=request.default,
            show_default=request.default is not None,
            prompt_suffix=": ",
        )

        context.resolve(
            request.name,
            value,
        ) 