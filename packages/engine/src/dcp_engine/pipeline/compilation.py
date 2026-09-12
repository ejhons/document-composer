from pathlib import Path

from dcp_engine.runtime.context import EngineContext
from dcp_engine.runtime.execution.session import ExecutionSession
from dcp_engine.runtime.logging.log import logger


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
        self.last_generated_file : Path | None = None


    def execute(
        self,
        session:ExecutionSession,
        target_format: str
    ) -> ExecutionSession:
        # target_format = session.manifest.target_format
        # print("road", target_format)
        if target_format=='default':
            target_format = session.manifest.target_format
            
        logger.info(f'[{session.id}]: Compiling format: {target_format}')
        compiler = self.compiler_registry.get(target_format)

        output_path_object = session.workspace.dir_from_root(
            relative_dir=self.output_path + '/' + self.output_name + '.' + target_format,
            exists_ok=True
        )
        logger.info(f'[{session.id}]: Compiling output: {output_path_object}')
        
        markdown = session.fragmented_markdown.assembled_content
        temp_path = session.workspace.dir_from_temp(
            self.temp_file_name,
            exists_ok=True
        )

        logger.info(f'[{session.id}]: Creating Building object...')
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        # temp_path.write_text(markdown, encoding="utf8")

        logger.info(f'[{session.id}]: Start compiling...')
        compiler.compile(
            session=session,
            # markdown=markdown,
            source_markdown_path=temp_path.as_posix(),
            output_path= output_path_object.as_posix()
        )        

        self.last_generated_file = output_path_object

        logger.info(f'[{session.id}]: Compiling finished in {output_path_object}')
        return session