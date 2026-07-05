from engine.common.models.recipe import ComponentConfig
from engine.frontend.syntax.directives import DirectiveCall
from engine.planner.planning_context import PlanningContext
from engine.planner.graph.graph import RecipeGraph
from engine.planner.graph.component_node import ComponentNode, Dependency
from engine.frontend.directives.base import BaseDirectiveHandler, DirectiveResolutionResult


class IncludeDirectiveHandler(BaseDirectiveHandler):

    @property
    def directive_name(self) -> str:
        return "include"

    def resolve(
        self,
        graph: RecipeGraph,
        current_node: ComponentNode,
        directive: DirectiveCall,
        context: PlanningContext
    ) -> DirectiveResolutionResult:

        if not directive.arguments:
            raise ValueError("@include requer um argumento.")

        # Captura o primeiro argumento
        source = context.resource_resolver.normalize(
            current=current_node.component,
            source=directive.arguments[0].expression.source
            )
        # Verifica se o nó existe no grafo para evitar criar duplicatas.
        existing = graph.find_by_source(source)

        result = DirectiveResolutionResult()
        # print(self._infer_format(source), source)
        if existing is None:
            component = ComponentConfig(
                # id=source,
                type="external",
                source=source,
                # file_format=self._infer_format(source)
            )

            existing = ComponentNode(component=component)
            # graph.add_node(existing)
            result.created_nodes.append(existing)

        dependency = Dependency(
            source_id=current_node.id,
            target_id=existing.id,
            kind='directive'
        )
        # graph.add_dependency(dependency)
        result.dependencies.append(dependency)
        return result
        #     current_node.id,
        #     existing.id
        # )

    # def _infer_format(self, source: str) -> str:
    #     return source.split(".")[-1]