
from pydantic import BaseModel, Field

from engine.frontend.syntax.expressions.parser import ExpressionParser
from engine.frontend.syntax.fields import FieldDefinition
from engine.frontend.syntax.variables import VariableReference
from engine.planner.graph.component_node import ComponentNode
from engine.planner.graph.graph import RecipeGraph


class PendingCollector:
    def collect(
        self, 
        # node: ComponentNode,
        graph: RecipeGraph,
        ) -> PendingResolution:
        result = PendingResolution()

        for node in graph.nodes.values():
            resolution = node.resolution

            resolution.pending_inputs.clear()
            resolution.pending_dependencies.clear()

            for variable in node.inspection.variables:
                required_inputs = ExpressionParser.discover_inputs(variable.name)

                for input_name in required_inputs:
                    if input_name not in resolution.resolved_inputs:
                        resolution.pending_inputs.add(input_name)
                        result.pending_inputs[input_name] = PendingInput(name=input_name)
            
            for dependency_id in resolution.dependencies:
                dependency = graph.nodes.get(dependency_id)

                if dependency is None:
                    resolution.pending_dependencies.add(dependency_id)
                    continue

                if not dependency.resolution.resolved:
                    resolution.pending_dependencies.add(dependency_id)
                    result.pending_dependencies[dependency.id] = PendingDependency(node_id=dependency.id)

            #
            # Resultado
            #
            # result = PendingResolution(
            #     pending_inputs=set(resolution.pending_inputs),
            #     pending_dependencies=set(resolution.pending_dependencies),
            # )

            # node.resolution.resolved = result.resolved
        return result
        
        
class PendingResolution(BaseModel):
    pending_inputs: dict[str, PendingInput] = Field(default_factory=dict)
    pending_dependencies: dict[str, PendingDependency] = Field(default_factory=dict)

    @property
    def has_pending_inputs(self) -> bool:
        return bool(self.pending_inputs)

    @property
    def has_pending_dependencies(self) -> bool:
        return bool(self.pending_dependencies)

    @property
    def resolved(self) -> bool:
        return (
            not self.pending_inputs and
            not self.pending_dependencies
        )
    
# class PendingResolution:
#     pending_inputs: set[str] = Field(default_factory=set)
#     pending_dependencies: set[str] = Field(default_factory=set)

#     @property
#     def has_pending_inputs(self) -> bool:
#         return bool(self.pending_inputs)

#     @property
#     def has_pending_dependencies(self) -> bool:
#         return bool(self.pending_dependencies)

#     @property
#     def resolved(self) -> bool:
#         return (
#             not self.pending_inputs and
#             not self.pending_dependencies
#         )
    
class PendingInput(BaseModel):
    name: str
    reason: str = "Input not provided"

class PendingDependency(BaseModel):
    node_id: str
    reason: str = "Dependency not resolved"
