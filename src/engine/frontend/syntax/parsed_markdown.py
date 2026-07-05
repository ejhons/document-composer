
from typing import Any

from pydantic import BaseModel

from engine.frontend.syntax.fields import FieldDefinition
from engine.frontend.syntax.directives import DirectiveCall
from engine.frontend.syntax.variables import VariableReference


class ParsedMarkdown(BaseModel):
    metadata: dict[str, Any]          # sem a chave "fields"
    fields: dict[str, FieldDefinition]
    variables: list[VariableReference]
    directives: list[DirectiveCall]
    body: str

    @property
    def unique_variables(self) -> dict[str, VariableReference]:
        return {
            ref.expression: ref
            for ref in self.variables
        }
    
    @property
    def variable_names(self) -> set[str]:
        return set([
            ref.expression
            for ref in self.variables
            ])

    # metadata:dict[str, Any]
    # body: str
    # fields: dict[str, FieldDefinition]
    # variables: list[VariableReference]
    # directives: list[DirectiveCall]
