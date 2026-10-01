
import shutil
from pathlib import Path
from dcp_engine.compilation.compilers.base import BaseCompiler
from dcp_engine.runtime.execution.session import ExecutionSession


class MarkdownCompiler(BaseCompiler):
    def compile(
        self,
        session: ExecutionSession,
        source_markdown_path: str,
        output_path: str,
    ) -> str:       
        # if not self.registry: 
        #     print("[Compiler - DOCX Warning] Input adapter for 'docx' merge not found in injected registry.")
        shutil.copy(
            src=source_markdown_path,
            dst=output_path
        )
        return Path(output_path)