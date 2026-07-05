from abc import ABC, abstractmethod
from engine.common.models.recipe import ComponentConfig
from engine.common.models.inspection import InspectionResult

inspection_registry:dict[str, BaseOjbjectInspector] = {}

class BaseOjbjectInspector(ABC):

    @abstractmethod
    def inspect(self, component:ComponentConfig) -> InspectionResult:
        ...
