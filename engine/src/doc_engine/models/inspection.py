from typing import Literal
from pydantic import BaseModel, Field
from engine.src.doc_engine.models.runtime import DirectiveCall, VariableReference


class InspectionResult(BaseModel):
    variables: set[VariableReference] = Field(default_factory=set) # type: ignore
    directives: list[DirectiveCall] = Field(default_factory=list) # type: ignore
    diagnostics: list[Diagnostic] = Field(default_factory=list)
    metadata:dict[str, str] = Field(default_factory=dict)

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
    