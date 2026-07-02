from engine.src.doc_engine.analysis.directives.registry import DirectiveRegistry
from engine.src.doc_engine.analysis.inspectors.registry import StaticInspectorRegistry
from engine.src.doc_engine.models.inspection import InspectionResult
from engine.src.doc_engine.planning.recipe.recipe_graph import RecipeGraph
from engine.src.doc_engine.planning.recipe.component_node import ComponentNode

class DependencyResolver:
    def __init__(
        self,
        graph: RecipeGraph,
        inspector_registry: StaticInspectorRegistry,
        directive_registry: DirectiveRegistry
    ):
        self.graph = graph
        self.registry = inspector_registry
        self.directive_registry:dict = directive_registry

    def resolve(self) -> RecipeGraph:
        queue: list[ComponentNode] = list(self.graph.nodes.values())
        visited = set()

        while queue:
            node = queue.pop(0)
            # Garante que o mesmo nó não seja adicionado mais de uma vez
            if node.id in visited:
                continue

            visited.add(node.id)
            inspector = self.registry.get(node.component.file_format)

            if inspector is None:
                continue

            inspection:InspectionResult = inspector.inspect(node.component)
            node.variables.update(inspection.variables)

            for directive in inspection.directives:
                handler = self.directive_registry.get(directive.name)

                if handler is None:
                    continue

                # Handler faz a edição no grado adicionando nós e dependências
                result = handler.resolve(
                    self.graph,
                    node,
                    directive
                )
                # Adiciona os nós criados para manter a pilha e verificar se eles não possuem dependências.
                queue.extend(result.created_nodes)

        return self.graph
    
    # def _resolve_dependency(
    #     self,
    #     parent: ComponentNode,
    #     dependency: DependencyReference,
    #     queue: list[ComponentNode]
    # ):
    #     if dependency.dynamic:
    #         return
    #     existing = self.graph.find_by_source(dependency.expression)
    #     child = ComponentNode.from_reference(
    #         dependency
    #     )

    #     self.graph.add_node(child)

    #     queue.append(child)
    #     self.graph.add_dependency(
    #         parent.id,
    #         child.id
    #     )