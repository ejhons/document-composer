from pathlib import Path

from engine.common.models.recipe import ComponentConfig
from engine.planner.resources.base import ResourceResolver


class LocalResourceResolver(ResourceResolver):
    def normalize(
            self,
            current: ComponentConfig,
            source: str
        ) -> str:
        
        source = (
            Path(current.source)
            .parent
            .joinpath(source)
            .resolve()
            .as_posix()
        )
        return source
        # return Path(source).resolve().as_posix()

    def resolve(
        self,
        current: ComponentConfig,
        source: str
    ):
        # source = (
        #     Path(current.source)
        #     .parent
        #     .joinpath(source)
        #     .resolve()
        #     .as_posix()
        # )
        # return source
        current.source = self.normalize(current, source)