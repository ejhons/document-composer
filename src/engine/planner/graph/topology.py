from typing import Iterator
from collections import deque
from engine.planner.graph.component_node import ComponentNode


class Topology():
    def executable_nodes(self) ->  Iterator[ComponentNode]:
        return iter(self.topological_order())
    
    def topological_order(self) -> list[ComponentNode]:
        """
        Retorna os nós em ordem topológica.
        Utiliza o método de Kahn para ordenação do grafo.
        Raises:
            ValueError caso exista um ciclo.
        """
        indegree = {
            node_id: 0
            for node_id in self.nodes
        }

        adjacency = {
            node_id: []
            for node_id in self.nodes
        }

        for edge in self.edges:
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
            result.append(self.nodes[node_id])
            for dependent in adjacency[node_id]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(self.nodes):
            raise ValueError(
                "Cyclic occurence in graph"
            )

        return result

