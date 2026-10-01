# from engine.common.models.placeholder import NodePlaceholder
from dcp_engine.language.directives.base import BaseDirectiveHandler
from dcp_engine.language.directives.result import DirectiveResolutionResult
from dcp_engine.language.manifests.recipe import ComponentConfig
from dcp_engine.language.syntax.directives import DirectiveCall
from dcp_engine.solving.solving_context import SolvingContext
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.planning.graph.component_node import ComponentNode, Dependency


class IncludeDirectiveHandler(BaseDirectiveHandler):

    @property
    def directive_name(self) -> str:
        return "include"

    def resolve(
        self,
        graph: RecipeGraph,
        current_node: ComponentNode,
        directive: DirectiveCall,
        context: SolvingContext
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
            result.created_nodes.append(existing)

        dependency = Dependency(
            source_id=current_node.id,
            target_id=existing.id,
            kind='directive',
            origin = str(directive.index)
        )
        # graph.add_dependency(dependency)

        # result.resolved = True
        result.dependencies.append(dependency)

        # if not current_node.resolution.resolved_inputs:
        #     result.placeholder = NodePlaceholder(node_id=existing.id)#f'__dc:node:{existing.id}__'
            
        return result
        #     current_node.id,
        #     existing.id
        # )

    # def _infer_format(self, source: str) -> str:
    #     return source.split(".")[-1]