from engine.common.models.directives_result import DirectiveResolutionResult
from engine.common.models.inspection_result import InspectionResult
from engine.frontend.parser import MarkdownParser
from engine.planning.graph.component_node import ComponentNode
from engine.planning.graph.graph import RecipeGraph
from engine.planning.solving_context import SolvingContext
# from engine.planner.planning_context import PlanningContext
# from engine.runtime.context import EngineContext

class DependencyResolver:
    '''
    Recebe Graph e PlanningContext
    Executa diretivas e adiciona nós criados ao Graph
    Atualiza dependências na resolution
    Resolve as diretivas de cada componente.

    Responsabilidades:
    - Criar nós gerados pelas diretivas;
    - Criar dependências no grafo;
    - Atualizar ResolutionState.dependencies;
    - Substituir diretivas resolvidas por placeholders estáveis.
    '''
    def __init__(
            self,
            markdown_parser: MarkdownParser | None = None
        ):
        self.markdown_parser = markdown_parser or MarkdownParser()

        
    def resolve(
            self,
            graph: RecipeGraph,
            context:SolvingContext
        ):
        visited: set[str] = set()
        queue: list[ComponentNode] = list(graph.nodes.values())

        while queue:
            node = queue.pop(0)
            # Garante que o mesmo nó não seja adicionado mais de uma vez
            if node.id in visited:
                continue

            visited.add(node.id)
            resolution = node.resolution

            if not resolution.changed:
                continue

            if not resolution.content:
                resolution.content = node.inspection.body if node.inspection else None

            resolution.dependencies.clear()
            # created_nodes = 
            self._resolve_node(
                node=node,
                graph=graph,
                context=context
            )
            # queue.extend(created_nodes)
            resolution.changed = False

    # Adiciona os nós criados para manter a pilha e verificar se eles não possuem dependências.
    def _resolve_node(
            self,
            node: ComponentNode,
            graph: RecipeGraph,
            context:SolvingContext
        ) -> list[ComponentNode]:

        resolution = node.resolution
        if resolution is None:
            return []
        
        if resolution.content is None:
            return []

        created_nodes: list[ComponentNode] = []
        directives = self.markdown_parser.extract_directives(
            resolution.content
        )

        # content = resolution.content
        for directive in directives:
            handler = context.directive_registry.get(directive.name)

            if handler is None:
                continue

            # Handler faz a edição no grafo adicionando nós e dependências
            result: DirectiveResolutionResult = handler.resolve(
                graph=graph,
                current_node=node,
                directive=directive,
                context=context
            )

            #
            # Atualiza o grafo
            #
            for created_node in result.created_nodes:
                graph.add_node(created_node)
                created_nodes.append(created_node)
                # queue.append(created_node) #Removido porque 
                
            for dependency in result.dependencies:
                graph.add_dependency(dependency)
                node.resolution.dependencies.add(dependency.target_id)

            # Somente substitui quando a diretiva foi resolvida.
            # if result.placeholder:
            #     content = content.replace(
            #         directive.raw,
            #         result.replacement,
            #         1,
            #     )

        # resolution.content = content

        return created_nodes

            # directives = self.markdown_parser.extract_directives(
            #     resolution.content
            # )

            # for directive in directives:
            #     handler = context.directive_registry.get(directive.name)

            #     if handler is None:
            #         continue

            #     # Handler faz a edição no grado adicionando nós e dependências
            #     result = handler.resolve(
            #         graph=graph,
            #         current_node=node,
            #         directive=directive,
            #         context=context
            #     )

            #     for created_node in result.created_nodes:
            #         graph.add_node(created_node)
            #         # queue.append(created_node) #Removido porque 
                    
            #     for dependency in result.dependencies:
            #         graph.add_dependency(dependency)
            #         node.resolution.dependencies.add(
            #             dependency.target_id
            #         )

