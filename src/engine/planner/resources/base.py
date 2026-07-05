from abc import ABC, abstractmethod
from engine.common.models.recipe import ComponentConfig


class ResourceResolver(ABC):
    @abstractmethod
    def normalize(self, source: str) -> str:
        ...

    @abstractmethod
    def resolve(
        self,
        current: ComponentConfig,
        reference: str
    ) -> str:
        ...