from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class FileRepository(ABC):

    @abstractmethod
    def list(self, project_id: str) -> list[Path]:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        project_id: str,
        filename: str,
        content: bytes,
    ) -> Path:
        raise NotImplementedError

    @abstractmethod
    def read(
        self,
        project_id: str,
        filename: str,
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        project_id: str,
        filename: str,
    ) -> None:
        raise NotImplementedError


class FileService:

    def __init__(self, repository: FileRepository) -> None:
        self._repository = repository

    def list_files(self, project_id: str) -> list[Path]:
        return self._repository.list(project_id)

    def save_file(
        self,
        project_id: str,
        filename: str,
        content: bytes,
    ) -> Path:
        self._validate_filename(filename)

        if not content:
            raise ValueError("File cannot be empty.")

        return self._repository.save(
            project_id,
            filename,
            content,
        )

    def read_file(
        self,
        project_id: str,
        filename: str,
    ) -> bytes:
        self._validate_filename(filename)

        return self._repository.read(
            project_id,
            filename,
        )

    def delete_file(
        self,
        project_id: str,
        filename: str,
    ) -> None:
        self._validate_filename(filename)

        self._repository.delete(
            project_id,
            filename,
        )

    @staticmethod
    def _validate_filename(filename: str) -> None:
        path = Path(filename)

        if not filename.strip():
            raise ValueError("Filename cannot be empty.")

        if path.is_absolute():
            raise ValueError("Absolute paths are not allowed.")

        if ".." in path.parts:
            raise ValueError(
                "Parent directory traversal is not allowed."
            )