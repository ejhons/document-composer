from engine.backend.compilers.registry import CompilerRegistry
from engine.runtime.context import EngineContext
from engine.runtime.execution.session import ExecutionSession


class CompilationModule:

    def __init__(
        self,
        context: EngineContext
        # compiler_registry: CompilerRegistry
    ):
        self.compilers = context.compiler_registry

    def compile(
        self,
        session:ExecutionSession,
        output_path
    ):
        target_format = session.manifest.target_format
        compiler = self.compilers.get_compiler(target_format)
        compiler.compile(
            fragmented = session.fragmented_markdown,
            output_path= output_path
        )
        

        return compiler.compile(
            document=document,
            output_path=output_path
        )