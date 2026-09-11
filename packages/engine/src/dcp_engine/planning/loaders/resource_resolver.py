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

        source_path = (
            root
            .joinpath(source)
            .resolve()
        )

        if not source_path.is_relative_to(root.resolve()):
            raise ValueError("Resource escapes workspace")

        
        print(root)
        print(source)
        print(current.source)
        return source_path.as_posix()
        # return Path(source).resolve().as_posix()

    def resolve(
        self,
        current: ComponentConfig,
        source: str,
        *,
        root: Path | str | None = None
    ) -> str:
        source_path = Path(source)
        # Absolute
        if source_path.is_absolute():
            source_normalized = source            
        # Relative
        else:
            source_normalized = self.normalize(current, source, root)
        
        current.source = source_normalized# self.normalize(current, source, root)
        return current.source