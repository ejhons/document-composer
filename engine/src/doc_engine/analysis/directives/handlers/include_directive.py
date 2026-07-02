from engine.src.doc_engine.models.runtime import DirectiveCall
from engine.src.doc_engine.models.recipe import ComponentConfig
from engine.src.doc_engine.planning.recipe.recipe_graph import RecipeGraph
from engine.src.doc_engine.planning.recipe.component_node import ComponentNode
from engine.src.doc_engine.analysis.directives.handlers.base import BaseDirectiveHandler, DirectiveResolutionResult


class IncludeDirectiveHandler(BaseDirectiveHandler):

    @property
    def directive_name(self) -> str:
        return "include"

    def resolve(
        self,
        graph: RecipeGraph,
        current_node: ComponentNode,
        directive: DirectiveCall,
    ) -> DirectiveResolutionResult:

        if not directive.arguments:
            raise ValueError("@include requer um argumento.")

        source = directive.arguments[0].value
        existing = graph.find_by_source(source)

        result = DirectiveResolutionResult()
        if existing is None:
            component = ComponentConfig(
                id=source,
                type="external",
                source=source,
                file_format=self._infer_format(source)
            )

            existing = ComponentNode(component=component)
            graph.add_node(existing)
            result.created_nodes.append(existing)

        graph.add_dependency(
            current_node.id,
            existing.id
        )

    def _infer_format(self, source: str) -> str:
        return source.split(".")[-1]