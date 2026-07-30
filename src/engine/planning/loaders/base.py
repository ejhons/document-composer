from abc import ABC, abstractmethod
from engine.frontend.manifests.recipe import ComponentConfig


class ResourceResolver(ABC):
    '''
    ResourceResolve solves resources (files, links, etc)
    '''
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