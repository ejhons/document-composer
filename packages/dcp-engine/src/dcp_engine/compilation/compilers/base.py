from typing import Any, Optional
from abc import ABC, abstractmethod
# from engine.backend.compilers.registry import CompilerRegistry
# from engine.frontend.syntax.markdown.atomized_markdown import AtomizedMarkdown
from dcp_engine.runtime.execution.session import ExecutionSession

# =====================================================================
# 1. THE OUTPUT PORT (Abstract Base Class)
# =====================================================================
class BaseCompiler(ABC):
    """
    The Output Port contract for document generation.
    Every format exporter (Docx, Pdf, Html) must satisfy this interface.
    """
    def __init__(
            self,
            registry: Optional[Any] = None,
        ):
        # Recebe a injeção do registro de adaptadores se necessário
        self.registry = registry

    @abstractmethod
    def compile(
        self,
        session: ExecutionSession,
        output_path: str,
        markdown: str | None = None,
        **kwargs
    ) -> str:
        ...