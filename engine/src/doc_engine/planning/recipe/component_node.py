from typing import Any, Optional
from pydantic import BaseModel, Field
from engine.src.doc_engine.models.recipe import ComponentConfig
from engine.src.doc_engine.models.runtime import DirectiveCall, VariableReference


class ComponentNode(BaseModel):

    '''
    Elemento de execução que determina um ponto de execução da Pipeline.
    '''
    id: str
    component: ComponentConfig
    dependencies: set[str]
    dependents: set[str]
    artifact: Optional[str]
    context: dict[str, Any]
    completed: bool = False
    discovered: bool = False
    variables: set[VariableReference] = Field(default_factory=set) # type: ignore
    directives: list[DirectiveCall] = Field(default_factory=list) # type: ignore

class Dependency(BaseModel):
    source_id: str
    target_id: str
    kind: str
