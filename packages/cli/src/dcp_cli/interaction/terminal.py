from typing import Any
from dcp_application.ports import InteractionPort
import typer

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
        for key, request in pending.pending_inputs_definition.items():
            values[key] = self._prompt(request)

        return values

    
    def _prompt(self, request: InputDefinition) -> Any:
        '''
        Prompts for user answer
        '''
        prompt = request.label or request.name

        if request.description:
            prompt = f"{request.name} ({request.description})"

        return typer.prompt(
            prompt,
            default=request.default,
            show_default=request.default is not None,
            prompt_suffix=": ",
        )