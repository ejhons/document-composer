from pathlib import Path

from engine.frontend.manifests.recipe import ComponentConfig
from engine.planning.loaders.base import ResourceResolver


class LocalResourceResolver(ResourceResolver):
    '''
    Capaz de normalizar o endereço de componentes.
    '''
    def normalize(
            self,
            current: ComponentConfig,
            source: str
        ) -> str:
        '''
        Normaliza o endereço para um endereço global.
        '''        
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