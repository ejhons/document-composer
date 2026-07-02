from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from engine.src.doc_engine.models.directives import DirectiveResolutionResult
from engine.src.doc_engine.models.runtime import DirectiveCall
from engine.src.doc_engine.planning.recipe.recipe_graph import RecipeGraph
from engine.src.doc_engine.planning.recipe.component_node import ComponentNode

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
    ) -> DirectiveResolutionResult:
        ...
