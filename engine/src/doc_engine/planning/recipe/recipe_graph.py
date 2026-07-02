from enum import Enum
from typing import Iterator
from collections import deque
from pydantic import BaseModel, Field
from engine.src.doc_engine.exceptions import NodeAlreadyRegistered
from engine.src.doc_engine.planning.recipe.component_node import ComponentNode, Dependency


class VisitState(Enum):
    NOT_VISITED = 0
    VISITING = 1
    VISITED = 2


class RecipeGraph(BaseModel):
    nodes: dict[str, ComponentNode] = Field(default_factory=dict)
    edges: list[Dependency] = Field(default_factory=list)

    def add_node(self, node: ComponentNode):
        if node.id in self.nodes:
            raise NodeAlreadyRegistered(f'Node "{node.node_id}" already exists')
        self.nodes[node.node_id] = node

    def add_dependency(self, dependency: Dependency):
        self._validate_dependency(dependency)
        self._dependents_cache = None
        self.edges = dependency

    def children(self, node_id:str):
        return [
            self.nodes[edge.target_id] 
            for edge in self.edges 
            if edge.source_id == node_id
            ]

    def parents(self, node_id:str):
        return [
            self.nodes[edge.source_id] 
            for edge in self.edges 
            if edge.target_id == node_id
            ]

    def leaves(self):
        return [node for node in self.nodes if len(self.children(node.id)==0)]
    

    def roots(self):
        return [node for node in self.nodes if len(self.parents(node.id)==0)]
    

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
                "RecipeGraph possui dependências cíclicas."
            )

        return result



    def detect_cycles(self) -> bool:
        """
        Detecta ciclos no grafo de dependências.

        Returns:
            True caso exista algum ciclo.
        """

        adjacency: dict[str, list[str]] = {
            node_id: [] for node_id in self.nodes
        }

        for edge in self.edges:
            adjacency[edge.source_id].append(edge.target_id)

        state = {
            node_id: VisitState.NOT_VISITED
            for node_id in self.nodes
        }

        def dfs(node_id: str) -> bool:
            state[node_id] = VisitState.VISITING

            for child in adjacency[node_id]:

                if state[child] == VisitState.VISITING:
                    return True

                if (
                    state[child] == VisitState.NOT_VISITED
                    and dfs(child)
                ):
                    return True

            state[node_id] = VisitState.VISITED
            return False

        for node_id in self.nodes:
            if (
                state[node_id] == VisitState.NOT_VISITED
                and dfs(node_id)
            ):
                return True

        return False