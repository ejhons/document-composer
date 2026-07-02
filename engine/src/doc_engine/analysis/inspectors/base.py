from pathlib import Path
from abc import ABC, abstractmethod
from engine.src.doc_engine.models.recipe import ComponentConfig
from engine.src.doc_engine.models.inspection import InspectionResult

inspection_registry:dict[str, BaseOjbjectInspector] = {}

class BaseOjbjectInspector(ABC):

    @abstractmethod
    def inspect(self, component:ComponentConfig) -> InspectionResult:
        ...
