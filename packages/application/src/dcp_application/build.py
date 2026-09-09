from pathlib import Path

from doc_engine.core.engine import DocumentEngine
from doc_engine.core.execution import ExecutionResult


class BuildDocumentUseCase:

    def __init__(self, engine: DocumentEngine | None = None):
        self.engine = engine or DocumentEngine()

    def create_session(
        self,
        recipe_path: Path,
        output_path: Path | None = None,
    ):
        return self.engine.create_session(
            recipe_path=recipe_path,
            output_path=output_path,
        )

    def execute(self, session) -> ExecutionResult:
        return self.engine.execute(session)