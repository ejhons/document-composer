import pickle
from pathlib import Path

from dcp_api.application.iteraction import ExecutionSessionRepository
from dcp_api.domain.session import Session


class FileExecutionSessionRepository(ExecutionSessionRepository):

    def __init__(self, workspace: Path):
        self._workspace = workspace

    def _directory(
        self,
        project_id: str,
    ) -> Path:

        directory = (
            self._workspace
            / "projects"
            / project_id
            / ".sessions"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return directory

    def _path(
        self,
        project_id: str,
        session_id: str,
    ) -> Path:

        directory = (
            self._workspace
            / "projects"
            / project_id
            / ".sessions"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return directory / f"{session_id}.session"

    def save(self, session: Session) -> None:
        path = self._path(
            session.project_id,
            session.id,
        )

        #TODO: Atualizar serialização.
        with path.open("wb") as file:
            pickle.dump(session, file)

    def get(
        self,
        *,
        project_id: str,
        session_id: str,
    ) -> Session:
        path = self._path(
            project_id,
            session_id,
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Execution session '{session_id}' not found."
            )

        #TODO: Atualizar serialização.
        with path.open("rb") as file:
            return pickle.load(file)

    def close(
        self,
        *,
        project_id: str,
        session_id: str,
    ):
        
        path = self._path(
            project_id,
            session_id,
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Execution session '{session_id}' not found."
            )
        path.unlink(missing_ok=True)

    
    def list(
        self,
        *,
        project_id: str,
    ) -> list[Session]:
        dir = self._directory(
            project_id,
        )
        # Pega arquivos na pasta principal
        files_in_folder = list(dir.glob('*.session'))
        return [
            self.get(
                project_id=project_id,
                session_id=f.stem
            )
            for f in files_in_folder
        ]

    
    def close_all(
        self,
        *,
        project_id: str,
    ):        
        dir = self._directory(project_id)
        # Pega arquivos na pasta principal
        files_in_folder = list(dir.glob('*.session'))
        for f in files_in_folder:
            f.unlink(missing_ok=True)