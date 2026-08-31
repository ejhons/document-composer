from dcp_engine.runtime.context import EngineContext
from dcp_engine.runtime.execution.session import ExecutionSession


class CompilationModule:

    def __init__(
        self,
        context: EngineContext,
        output_path: str = 'output',
        output_name: str = 'generated_document',
        temp_file_name: str = 'temp_markdown.md'
    ):
        self.compiler_registry = context.compiler_registry
        self.output_path = output_path
        self.output_name = output_name
        self.temp_file_name = temp_file_name


    def execute(
        self,
        session:ExecutionSession,
        target_format: str | None = None
    ) -> ExecutionSession:
        target_format = target_format or session.manifest.target_format
        compiler = self.compiler_registry.get(target_format)

        output_path_object = session.workspace.dir_from_root(
            relative_dir=self.output_path + '/' + self.output_name + '.' + target_format,
            exists_ok=True
        )
        
        markdown = session.fragmented_markdown.assembled_content
        temp_path = session.workspace.dir_from_temp(
            self.temp_file_name,
            exists_ok=True
        )
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        # temp_path.write_text(markdown, encoding="utf8")

        compiler.compile(
            session=session,
            # markdown=markdown,
            source_markdown_path=temp_path.as_posix(),
            output_path= output_path_object.as_posix()
        )        

        return session