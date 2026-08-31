from abc import ABC, abstractmethod
from dcp_engine.language.manifests.recipe import ComponentConfig
from dcp_engine.solving.inspection.result import InspectionResult

inspection_registry:dict[str, BaseOjbjectInspector] = {}

class BaseOjbjectInspector(ABC):

    @abstractmethod
    def inspect(self, component:ComponentConfig) -> InspectionResult:
        ...
