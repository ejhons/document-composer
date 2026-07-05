from pydantic import BaseModel, Field
from engine.common.models.inspection import InspectionResult
from engine.common.models.recipe import ComponentConfig
from engine.common.utils.generator import IdGenerator
from engine.planner.graph.resolution_state import ResolutionState


class ComponentNode(BaseModel):
    '''
    Elemento de execução que determina um ponto de execução da Pipeline.
    '''
    component: ComponentConfig
    id: str = Field(default_factory = IdGenerator.generate)
    inspection: InspectionResult | None = InspectionResult()
    resolution: ResolutionState | None = ResolutionState()
    # resolved: bool = False
    # resolved_content: str | None = None

class Dependency(BaseModel):
    source_id: str
    target_id: str
    kind: str









    # completed: bool = False
    # discovered: bool = False
    # context: dict[str, Any] = Field(default_factory=dict)
    # dependencies: set[str]
    # dependents: set[str]
    # artifact: Optional[str]
    # fields: dict[str, FieldDefinition] = Field(default_factory=dict)
    # variables: list[VariableReference] = Field(default_factory=list) # type: ignore
    # directives: list[DirectiveCall] = Field(default_factory=list) # type: ignore


    # def apply_inspection(
    #     self,
    #     inspection: "InspectionResult"
    # ) -> None:

    #     self.fields = dict(inspection.fields)
    #     self.variables = list(inspection.variables)
    #     self.directives = list(inspection.directives)
        
