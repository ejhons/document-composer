from pathlib import Path

from dcp_api.api.schemas.files import DirectoryResponse, FileContentResponse, FilePathListResponse, FilePathResponse, PathResponse

class FilesMapper:
    def path_to_response(self, path: Path | str) -> PathResponse:
        if isinstance(path, str):
            path = Path(path)

        if path.is_dir():
            return self._directory_to_response(path)

        return self._filepath_to_response(path)

    def files_to_response(self, paths: list[Path | str]) -> FilePathListResponse:
        paths_response = [
            self.path_to_response(file)
            for file in paths
        ]
        return FilePathListResponse(
            files = paths_response
        )

    def _filepath_to_response(self, path: Path | str) -> FilePathResponse:
        if isinstance(path, str):
            path = Path(path)

        name = path.stem
        extension = path.suffix

        return FilePathResponse(
            path=path.as_posix(),
            name=name,
            extension=extension
        )

    def _directory_to_response(self, directory: Path | str) -> DirectoryResponse:
        if isinstance(path, str):
            path = Path(directory)

        name = path.name
        files = []
        dirs = []

        for item in path.iterdir():
            if item.is_dir():
                dirs.append(self._directory_to_response(item))
            else:
                files.append(self._filepath_to_response(item))

        return DirectoryResponse(
            name = name,
            files = files,
            dirs = dirs
        )


    def file_to_content_reponse(self, path: Path | str) -> FileContentResponse:
        if isinstance(path, str):
            path = Path(path)
        
        # 1. Garante que o arquivo existe e não é uma pasta
        if not path.is_file():
            raise Exception('Arquivo não pode ser lido')

        try:
            # 2. Tenta ler o arquivo como texto UTF-8
            content = path.read_text(encoding='utf-8')
            return FileContentResponse(
                path=path.as_posix(),
                content=content
            )
        except UnicodeDecodeError:
            # Se falhar na decodificação, significa que é um arquivo binário
            raise Exception('Arquivo não é um arquivo de texto')

from collections import defaultdict
class FileTreeMapper():
    def path_list_to_dict(self, path_list:list[Path | str]):
        ...

    def create_node(self):
        return defaultdict(self.create_node)

    def paths_to_tree(self, path_list:list[Path | str]):
        arvore = self.create_node()
        for path in path_list:
            if isinstance(path, Path):
                path = path.as_posix()
            # Remove barras no início/fim e divide o caminho nas pastas/arquivos
            parts = path.strip("/\\").split("/")
            
            # Navega/cria os nós recursivamente
            no_atual = arvore
            for parte in parts:
                no_atual = no_atual[parte]
                
        return arvore

    # Converte o defaultdict em um dict comum para facilitar visualização e serialização (ex: JSON)
    def to_dict(self, d):
        if isinstance(d, defaultdict):
            d = {k: self.to_dict(v) for k, v in d.items()}
        return d