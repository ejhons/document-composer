from engine.common.models.inspection import InspectionResult
from engine.frontend.parser import MarkdownParser
from engine.planner.graph.component_node import ComponentNode
from engine.planner.graph.graph import RecipeGraph
from engine.planner.planning_context import PlanningContext

class DependencyResolver:
    '''
    Recebe Graph e PlanningContext
    Executa diretivas e adiciona nós criados ao Graph
    '''
    def __init__(
            self,
            markdown_parser: MarkdownParser | None = None
        ):
        self.markdown_parser = markdown_parser or MarkdownParser()

        
    def resolve(
            self,
            graph: RecipeGraph,
            context: PlanningContext
        ) -> RecipeGraph:
        queue: list[ComponentNode] = list(graph.nodes.values())
        visited = set()

        while queue:
            node = queue.pop(0)
            # Garante que o mesmo nó não seja adicionado mais de uma vez
            if node.id in visited:
                continue

            visited.add(node.id)
            resolution = node.resolution
            if not resolution.content:
                resolution.content = node.inspection.body

            directives = self.markdown_parser.extract_directives(
                node.resolution.content
            )
            # Até então, o único inspector resgistrado é o de Markdown.
            # inspector = context.inspector_registry.get(node.component.file_format)

            # if inspector is None:
            #     continue

            # #Realiza a inspeção
            # inspection:InspectionResult = inspector.inspect(node.component)
            # # node.variables = inspection.variables
            # node.inspection = inspection

            for directive in directives:#node.inspection.directives:
                handler = context.directive_registry.get(directive.name)

                if handler is None:
                    continue

                # Handler faz a edição no grado adicionando nós e dependências
                result = handler.resolve(
                    graph=graph,
                    current_node=node,
                    directive=directive,
                    context=context
                )
                for created_node in result.created_nodes:
                    graph.add_node(created_node)
                # queue.extend(result.created_nodes)
                for dependency in result.dependencies:
                    graph.add_dependency(
                        # node.id,
                        dependency
                    )
                    node.resolution.dependencies.add(
                        dependency.target_id
                    )
                # Adiciona os nós criados para manter a pilha e verificar se eles não possuem dependências.

        return graph
    
    # def __init__(
    #     self,
    #     graph: BaseGraph,
    #     context: PlanningContext
    #     # inspector_registry: StaticInspectorRegistry,
    #     # directive_registry: DirectiveRegistry,
    #     # resource_solver: LocalResourceResolver | None = None
    # ):
    #     self.graph = graph
    #     self.context = context
    #     # self.registry = inspector_registry
    #     # self.directive_registry = directive_registry
    #     # self.resource_solver = resource_solver or LocalResourceResolver()

    # @property
    # def inspector_registry(self):
    #     return self.context.inspector_registry
    
    # @property
    # def directive_registry(self):
    #     return self.context.directive_registry
    
    # @property
    # def resource_solver(self):
    #     return self.context.resource_solver

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