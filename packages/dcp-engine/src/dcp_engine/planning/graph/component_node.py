from pydantic import BaseModel, Field
from dcp_engine.language.manifests.recipe import ComponentConfig
from dcp_engine.planning.graph.assets import ComponentContent
from dcp_engine.common.generator import IdGenerator
from dcp_engine.solving.inspection.result import InspectionResult
from dcp_engine.solving.resolution.resolution_state import ResolutionState


class ComponentNode(BaseModel):
    '''
    Elemento de execução que determina um ponto de execução da Pipeline.
    '''
    component: ComponentConfig
    id: str = Field(default_factory = IdGenerator.generate)
    # Result of inspection operation keeping diagnostics, variables, directives and etc.
    inspection: InspectionResult | None = None
    resolution: ResolutionState = ResolutionState()
    adapted: ComponentContent | None = None
    # After resolution, some artifacts as dependencies, revision and pending inputs and dependencies are defined.
    # resolved: bool = False
    # resolved_content: str | None = None

class Dependency(BaseModel):
    source_id: str
    target_id: str
    kind: str
    origin: str | None = None

ComponentNode.model_rebuild()







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
        
