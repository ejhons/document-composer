from itertools import chain
from typing import Any
from pydantic import BaseModel, Field, PrivateAttr
from engine.frontend.syntax.fields import InputDefinition
from engine.frontend.syntax.directives import DirectiveCall
from engine.frontend.syntax.inputs import InputReference


class ParsedMarkdown(BaseModel):
    body: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    fields: dict[str, InputDefinition] = Field(default_factory=dict)
    # variables: list[InputReference] = Field(default_factory=list)
    _directives_map: dict[int, DirectiveCall] = PrivateAttr(default_factory=dict)

    def find_directive_by_id(self, id:int):
        return self._directives_map.get(id, None)

    @property
    def variables(self):
        return [
            ref
            for field in self.fields.values()
            for ref in field.references
        ]
    
    @property
    def directives(self) -> list[DirectiveCall]:
        return list(self._directives_map.values())
    
    @directives.setter
    def directives(self, value: list[DirectiveCall]):
        self._directives_map = {
            directive.index : directive
            for directive in value
        }

        # self._directives_map[value.index] = value

    @property
    def unique_variables(self) -> dict[str, InputReference]:
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
