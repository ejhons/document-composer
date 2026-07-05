from abc import ABC, abstractmethod
# from pydantic import BaseModel, Field
from engine.frontend.syntax.directives import DirectiveCall
from engine.common.models.directives import DirectiveResolutionResult
# from engine.src.doc_engine.planning.context import PlanningContext
from engine.planner.graph.graph import RecipeGraph
from engine.planner.graph.component_node import ComponentNode

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
