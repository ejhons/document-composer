from abc import ABC, abstractmethod
from dcp_engine.language.directives.result import DirectiveResolutionResult
from dcp_engine.language.syntax.directives import DirectiveCall
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.planning.graph.component_node import ComponentNode

class BaseDirectiveHandler(ABC):

    @property
    @abstractmethod
    def directive_name(self) -> str:
        ...

    @abstractmethod
    def resolve(
        self,
        graph: RecipeGraph,
        current_node: ComponentNode,
        directive: DirectiveCall,
        context#: PlanningContext        
    ) -> DirectiveResolutionResult:
        ...
