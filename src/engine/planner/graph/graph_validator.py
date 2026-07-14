from enum import Enum

class VisitState(Enum):
    NOT_VISITED = 0
    VISITING = 1
    VISITED = 2

class GraphValidator():
    '''
    Validate a graph detecting cycles.
    '''
    def detect_cycles(self) -> bool:
        """
        Detecta ciclos no grafo de dependências.
        ---
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