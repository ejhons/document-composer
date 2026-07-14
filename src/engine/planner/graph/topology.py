from typing import Iterator
from collections import deque
from engine.planner.graph.component_node import ComponentNode
from engine.planner.graph.graph import RecipeGraph


class Topology():
    def executable_nodes(
        self,
        graph:RecipeGraph
    ) ->  Iterator[ComponentNode]:
        return iter(self.topological_order(graph))
    
    def topological_order(
        self,
        graph:RecipeGraph
    ) -> list[ComponentNode]:
        """
        Retorna os nós em ordem topológica.
        Utiliza o método de Kahn para ordenação do grafo.
        Raises:
            ValueError caso exista um ciclo.
        """
        indegree = {
            node_id: 0
            for node_id in graph.nodes
        }

        adjacency = {
            node_id: []
            for node_id in graph.nodes
        }

        for edge in graph.edges:
            adjacency[edge.target_id].append(edge.source_id)
            indegree[edge.source_id] += 1

        queue = deque(
            node_id
            for node_id, degree in indegree.items()
            if degree == 0
        )

        result: list[ComponentNode] = []

        while queue:
            node_id = queue.popleft()
            result.append(graph.nodes[node_id])
            for dependent in adjacency[node_id]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(graph.nodes):
            raise ValueError(
                "Cyclic occurence in graph"
            )

        return result

