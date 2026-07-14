
from dataclasses import Field
from typing import Any

from pydantic import BaseModel

from engine.frontend.syntax.fields import FieldDefinition
from engine.frontend.syntax.directives import DirectiveCall
from engine.frontend.syntax.variables import VariableReference


class ParsedMarkdown(BaseModel):
    body: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    fields: dict[str, FieldDefinition] = Field(default_factory=dict)
    variables: list[VariableReference] = Field(default_factory=list)
    _directives_map: dict[int, DirectiveCall] = Field(default_factory=dict)

    def find_directive_by_id(self, id:int):
        return self._directives_map.get(id, None)

    @property
    def directives(self) -> list[DirectiveCall]:
        return list(self._directives_map.values())
    
    @directives.setter
    def directives(self, value: DirectiveCall):
        self._directives_map[value.index] = value

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
