from typing import Any
from dcp_application.ports import InteractionPort
import typer
from rich import print
from rich.prompt import Prompt

from dcp_engine.language.syntax.fields import InputDefinition
from dcp_engine.solving.resolution.resolution_collector import PendingResolution


class TerminalInteraction(InteractionPort):

    @classmethod
    def default(cls):
        return cls()

    def resolve(
        self,
        pending: PendingResolution
    ) -> dict[str, Any]:        
        '''
        Resolves project variables, asking the answer to user.
        '''
        values: dict[str, Any] = {}
        for key, request in pending.pending_input_definitions.items():
            values[key] = self._prompt(request)

        return values

    
    def _prompt(self, request: InputDefinition) -> Any:
        '''
        Prompts for user answer
        '''
        prompt = request.label or request.name
        # print(request)

        if request.description:
            prompt = f"{request.name} ({request.description})"

        prompt = f"[bold yellow]{prompt}[/bold yellow]"

        return Prompt.ask(
            prompt,
            default=request.default,
            show_default=request.default is not None,
        )
        # return typer.prompt(
        #     prompt,
        #     default=request.default,
        #     show_default=request.default is not None,
        #     prompt_suffix=": "
        # )