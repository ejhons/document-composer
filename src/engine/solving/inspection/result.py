from typing import Any, Literal
from pydantic import BaseModel, Field
from engine.frontend.syntax.directives import DirectiveCall
from engine.frontend.syntax.fields import InputDefinition
from engine.frontend.syntax.inputs import InputReference

class InspectionResult(BaseModel):
    body: str | None = None
    fields: dict[str, InputDefinition] = Field(default_factory=dict)
    variables: list["InputReference"] = Field(default_factory=list) # type: ignore
    directives: list["DirectiveCall"] = Field(default_factory=list) # type: ignore
    diagnostics: list[Diagnostic] = Field(default_factory=list)
    metadata:dict[str, Any] = Field(default_factory=dict)

    def __bool__(self):
        return self.body is not None
    
    @property
    def unique_variables(self) -> dict[str, InputReference]:
        return {
            ref.name: ref
            for ref in self.variables
        }
    
    @property
    def variable_names(self) -> set[str]:
        return set([
            ref.name
            for ref in self.variables
            ])

class Diagnostic(BaseModel):
    severity: Literal[
        "warning",
        "error"
    ]
    message: str
    line: int


# class InspectElement(BaseModel):    
#     id: str
#     source_path: str
#     file_format: str
#     cache: str = None
#     inspect_elements:List[InspectElement] = Field(default_factory=list)

#     @property
#     def has_cache(self):
#         return self.cache is not None
    