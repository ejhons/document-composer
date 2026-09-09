from pathlib import Path

from dcp_engine.language.manifests.recipe import ComponentConfig
from dcp_engine.planning.loaders.base import ResourceResolver


class LocalResourceResolver(ResourceResolver):
    '''
    Capaz de normalizar o endereço de componentes.
    '''
    def normalize(
            self,
            current: ComponentConfig,
            source: str,
            root: Path | str | None = None
        ) -> str:
        '''
        Normaliza o endereço para um endereço global.
        '''
        if root is None:
            root =  Path(current.source).parent

        if isinstance(root, str):
            root = Path(str)

        source = (
            # Path(current.source)
            # .parent
            root
            .joinpath(source)
            .resolve()
            .as_posix()
        )
        print(root)
        print(source)
        print(current.source)
        return source
        # return Path(source).resolve().as_posix()

    def resolve(
        self,
        current: ComponentConfig,
        source: str,
        *,
        root: Path | str | None = None
    ) -> str:
        # source = (
        #     Path(current.source)
        #     .parent
        #     .joinpath(source)
        #     .resolve()
        #     .as_posix()
        # )
        # return source
        # print(root)
        current.source = self.normalize(current, source, root)
        return current.source