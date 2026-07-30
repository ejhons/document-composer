from engine.compilation.adapters.registry import AdapterRegistry
from engine.runtime.workspace import Workspace
from engine.planning.graph.graph import RecipeGraph

class AdaptationResolver:
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
            adapter_registry: AdapterRegistry
        ):
        self.adapter_registry = adapter_registry

        
    def resolve(
        self,
        graph: RecipeGraph,
        workspace: Workspace
    ):        
        for node in graph.nodes.values():
            format_type = node.component.file_format
            registry = self.adapter_registry.get(format_type)
            
            if registry is None:
                continue

            content = registry.convert(
                node=node, 
                workspace=workspace
            )
            node.adapted = content
