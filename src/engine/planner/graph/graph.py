from typing import Any
from pydantic import BaseModel, Field, PrivateAttr
from engine.common.exceptions import NodeAlreadyRegistered, NodeNotFoundException
from engine.planner.graph.component_node import ComponentNode, Dependency

class RecipeGraph(BaseModel):
    edges: list[Dependency] = Field(default_factory=list)
    nodes: dict[str, ComponentNode] = Field(default_factory=dict)
    _source_index: dict[str, str]  = PrivateAttr(default_factory=dict)
    # _dependents_cache: dict[str, str]  = PrivateAttr(default_factory=dict)

    
    def get_node(self, node_id: str) -> ComponentNode:
        return self.nodes.get(node_id)

    
    def add_node(self, node: ComponentNode):
        '''
        O ComponentConfig em ComponentNode deve ter seu source normalizado.
        '''
        if node.id in self.nodes:
            raise NodeAlreadyRegistered(f'Node "{node.id}" already exists')
        
        self.nodes[node.id] = node
        self._source_index[node.component.source] = node.id

    def add_dependency(self, dependency: Dependency):
        self._validate_dependency(dependency)
        self.edges.append(dependency)
    
    def get_dependency(self, node_id: str) -> list[Dependency]:
        return [dep for dep in self.edges if dep.source_id==node_id]

    def _validate_dependency(self, dependency: Dependency):
        if dependency.source_id not in self.nodes:
            raise NodeNotFoundException(f'Source Node {dependency.source_id} must be in Graph for creating dependency')
        
        if dependency.target_id not in self.nodes:
            raise NodeNotFoundException(f'Target Node {dependency.target_id} must be in Graph for creating dependency')
        
    def has_direct_dependency(
            self, 
            source_id: str,
            target_id: str
        ) -> bool:
        visited = set()
        def dfs(node_id: str):
            if node_id == target_id:
                return True

            visited.add(node_id)
            for child in self.children(node_id):
                if child.id in visited:
                    continue

                if dfs(child.id):
                    return True

            return False
        return dfs(source_id)

    def has_dependency(
            self, 
            source_id: str,
            target_id: str
        ) -> bool:

        return any(
            edge.source_id == source_id
            and edge.target_id == target_id
            for edge in self.edges
        )

    @property
    def solved(self):
        return all(
            [node.resolution.resolved for node in self.nodes.values()]
        )


    def find_by_source(self, source: str):
        node_id = self._source_index.get(source)
        if node_id is None:
            return None

        return self.nodes[node_id]

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

    @property
    def leaves(self):
        return [node for node in self.nodes.values() if len(self.children(node.id))==0]
    
    @property
    def roots(self):
        return [node for node in self.nodes.values() if len(self.parents(node.id))==0]


class SolvedGraph(RecipeGraph):
    pass

RecipeGraph.model_rebuild()