from collections import deque

from engine.src.doc_engine.models.models import ComponentConfig, RecipeManifest

class SequencialTopology:
    @staticmethod
    def solve_dependencies(
        component:ComponentConfig,
        content
    ):



    @staticmethod
    def sort(
        manifest:RecipeManifest,
        
        ) -> list[str]:

        in_degree = {
            node_id: 0
            for node_id in manifest.components
        }

        # calcula graus de entrada
        # in_degree = {
        #     node_id: len(
        #         manifest.dependencies.get(
        #             node_id,
        #             []
        #         )
        #     )
        #     for node_id
        #     in graph.nodes
        # }

        # Cria pilha de nós para execução (Apenas nos nós raíz)
        queue = deque([
            node_id
            for node_id, degree
            in in_degree.items()
            if degree == 0
        ])

        # Itera sobre os ids dos nós
        result = []
        while queue:
            current = queue.popleft()
            result.append(current)

            downstream = (
                graph.get_downstream_nodes(
                    current
                )
            )
            
            for child in downstream:
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    queue.append(child)

        # ciclo
        # if len(result) != len(graph.nodes):
        #     raise RuntimeError(
        #         f'Ciclo detectado no grafo {len(result)} <> {len(graph.nodes)}'
        #     )

        return result