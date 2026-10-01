from abc import ABC, abstractmethod
from pathlib import Path

from dcp_engine.language.manifests.recipe import ComponentConfig



class ResourceResolver(ABC):
    '''
    ResourceResolve solves resources (files, links, etc)
    '''
    @abstractmethod
    def normalize(
        self,
        current: ComponentConfig,
        source: str,
        root: Path | str | None = None
    ) -> str:
        ...

    @abstractmethod
    def resolve(
        self,
        current: ComponentConfig,
        source: str,
        *,
        root: Path | str | None = None
    ) -> str:
        ...