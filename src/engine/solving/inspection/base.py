from abc import ABC, abstractmethod
from engine.frontend.manifests.recipe import ComponentConfig
from engine.solving.inspection.inspection_result import InspectionResult

inspection_registry:dict[str, BaseOjbjectInspector] = {}

class BaseOjbjectInspector(ABC):

    @abstractmethod
    def inspect(self, component:ComponentConfig) -> InspectionResult:
        ...
