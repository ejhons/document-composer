from pydantic import BaseModel
from engine.planner.graph.component_node import ComponentNode
from engine.planner.graph.graph import RecipeGraph
from engine.frontend.syntax.expressions.parser import ExpressionParser
from engine.planner.resolution.resolution_state import ResolutionState


class PendingCollector:
    '''
    Catching dependencies. 
    It could be used after solving dependencies.
    '''
    def collect(
        self,
        graph: RecipeGraph,
    ) -> PendingResolution:
        
        for node in graph.nodes.values():
            # Calcula pendências
            resolution = node.resolution
            if not resolution:
                continue

            resolution.pending_inputs.clear()
            resolution.pending_dependencies.clear()

            # if node.inspection is not None and node.inspection:
            self.collect_variables(node, resolution)
            
            # if not node.resolution.content:
            #     node.resolution.content = node.inspection.body if node.inspection else None
                      
            # if node.resolution.content is not None:
            self.collect_dependencies(graph, resolution)

            # for variable in node.inspection.variables:
            #     required_inputs = ExpressionParser.discover_inputs(variable.name)

            #     for input_name in required_inputs:
            #         if input_name in resolution.resolved_inputs:
            #             continue
            #         resolution.pending_inputs.add(input_name)
            
            # for dependency_id in resolution.dependencies:
            #     dependency = graph.nodes.get(dependency_id)

            #     if dependency is None:
            #         resolution.pending_dependencies.add(dependency_id)
            #         continue

            #     if not dependency.resolution.resolved:
            #         resolution.pending_dependencies.add(dependency_id)
            #         # result.pending_dependencies[dependency.id] = PendingDependency(node_id=dependency.id)
        resolved = all(
            node.resolution.resolved
            for node in graph.nodes.values()
        )
        unchanged =  all(
            not node.resolution.changed
            for node in graph.nodes.values()
        )

        return PendingResolution(
            resolved=resolved,
            unchanged=unchanged
        )
        
    def collect_variables(
            self,
            node: ComponentNode,
            resolution: ResolutionState
    ):
        if not node.inspection:
            return
        
        for variable in node.inspection.variables:
            required_inputs = ExpressionParser.discover_inputs(variable.name)

            for input_name in required_inputs:
                if input_name in resolution.resolved_inputs:
                    continue
                resolution.pending_inputs.add(input_name)

    def collect_dependencies(
            self,
            graph: RecipeGraph,
            resolution: ResolutionState
    ):
        if resolution is None:
            return

        for dependency_id in resolution.dependencies:
            dependency = graph.nodes.get(dependency_id)

            if dependency is None:
                resolution.pending_dependencies.add(dependency_id)
                continue

            if not dependency.resolution.resolved:
                resolution.pending_dependencies.add(dependency_id)
        
class PendingResolution(BaseModel):
    resolved: bool
    unchanged: bool

    
    # pending_inputs: dict[str, PendingInput] = Field(default_factory=dict)
    # pending_dependencies: dict[str, PendingDependency] = Field(default_factory=dict)

    # @property
    # def has_pending_inputs(self) -> bool:
    #     return bool(self.pending_inputs)

    # @property
    # def has_pending_dependencies(self) -> bool:
    #     return bool(self.pending_dependencies)

    # @property
    # def resolved(self) -> bool:
    #     return (
    #         not self.pending_inputs and
    #         not self.pending_dependencies
    #     )
    
# class PendingInput(BaseModel):
#     name: str
#     reason: str = "Input not provided"

# class PendingDependency(BaseModel):
#     node_id: str
#     reason: str = "Dependency not resolved"
