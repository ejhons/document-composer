from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4
from warnings import deprecated

from dcp_api.domain.iteraction import (
    IterationSession,
    IterationStatus,
    PendingResolution,
    ResolutionKind,
)

@deprecated
class FilesystemIterationRepository:
    FILE_NAME = "iteration.json"

    def __init__(self, workspace):
        self._workspace = workspace

    def create(
        self,
        project_id: str,
    ) -> IterationSession:

        session = IterationSession(
            id=uuid4().hex,
            project_id=project_id,
        )

        self.save(session)

        return session

    def get(
        self,
        project_id: str,
        session_id: str,
    ) -> IterationSession:

        path = self._path(
            project_id,
            session_id,
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Iteration session not found: "
                f"{session_id}"
            )

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return IterationSession(
            id=data["id"],
            project_id=data["project_id"],
            status=IterationStatus(data["status"]),
            variables=data.get(
                "variables",
                {},
            ),
            pending=[
                PendingResolution(
                    id=item["id"],
                    kind=ResolutionKind(
                        item["kind"]
                    ),
                    name=item["name"],
                    description=item.get(
                        "description"
                    ),
                    required=item.get(
                        "required",
                        True,
                    ),
                    metadata=item.get(
                        "metadata",
                        {},
                    ),
                )
                for item in data.get(
                    "pending",
                    [],
                )
            ],
            metadata=data.get(
                "metadata",
                {},
            ),
        )

    def save(
        self,
        session: IterationSession,
    ) -> None:

        path = self._path(
            session.project_id,
            session.id,
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                asdict(session),
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

    def delete(
        self,
        project_id: str,
        session_id: str,
    ) -> None:

        path = self._path(
            project_id,
            session_id,
        )

        if path.exists():
            path.unlink()

    def _path(
        self,
        project_id: str,
        session_id: str,
    ) -> Path:

        return (
            self._workspace
            .project_path(project_id)
            / ".iteration"
            / session_id
            / self.FILE_NAME
        )