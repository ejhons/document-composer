from __future__ import annotations

from pathlib import Path


class Workspace:
    """
    Representa o espaço de trabalho utilizado pelo Document Composer.

    Responsável exclusivamente pela organização física
    dos diretórios da aplicação.
    """

    PROJECTS_DIRECTORY = "projects"
    PROJECTS_DIRECTORY = "projects"
    OUTPUT_PROJECTS_DIRECTORY = "output"
    COMPONENTS_PROJECTS_DIRECTORY = "components"
    BASE_COMPONENTS_DIRECTORY = "base"

    def __init__(self, root: Path) -> None:
        self._root = root.expanduser().resolve()

    @property
    def root(self) -> Path:
        return self._root

    @property
    def projects(self) -> Path:
        return self._root / self.PROJECTS_DIRECTORY

    @property
    def base(self) -> Path:
        return self._root / self.BASE_COMPONENTS_DIRECTORY

    def initialize(self) -> None:
        """
        Garante que a estrutura básica do workspace exista.
        """
        self._root.mkdir(parents=True, exist_ok=True)
        self.base.mkdir(parents=True, exist_ok=True)
        self.projects.mkdir(parents=True, exist_ok=True)

    def project_path(self, project_id: str) -> Path:
        """
        Retorna o diretório físico de um projeto.
        """
        return self.projects / project_id

    def initialize_project(self, project_id: str) -> Path:
        project_path = self.project_path(project_id)

        project_path.mkdir(parents=True, exist_ok=False)
        (project_path / self.COMPONENTS_PROJECTS_DIRECTORY).mkdir()
        (project_path / self.OUTPUT_PROJECTS_DIRECTORY).mkdir()

        return project_path