from engine.runtime.engine import Engine
from engine.modules.planning import PlanningModule
from engine.modules.solving import SolvingModule
from engine.modules.assembling import AssemblingModule
from engine.modules.compilation import CompilationModule
from engine.runtime.context import EngineContext
from engine.backend.adapters.implementations.docx_adapter import DocxAdapter
from engine.backend.adapters.implementations.excel_adapter import ExcelToMarkdownAdapter
from engine.backend.adapters.implementations.image_adapter import ImageMarkdownAdapter
from engine.backend.adapters.implementations.md_adapter import MarkdownAdapter
from engine.backend.adapters.implementations.pdf_adapter import PdfToImageMarkdownAdapter
from engine.backend.compilers.implementations.docx_compiler import DocxCompiler
from engine.backend.compilers.implementations.html_compiler import HtmlCompiler
from engine.backend.compilers.implementations.pdf_compiler import PdfCompiler
from engine.frontend.directives.implementations.include_directive import IncludeDirectiveHandler
from engine.frontend.inspectors.implementations.inspector import MarkdownInspector
from engine.planner.resources.resource_resolver import LocalResourceResolver


class EngineBuilder:

    def __init__(self):
        self.context = EngineContext(
            resource_resolver=LocalResourceResolver()
        )


    def add_inspector(
        self,
        extension: str,
        inspector
    ) -> "EngineBuilder":
        self.context.inspector_registry.register(
            extension,
            inspector
        )
        return self


    def add_directive(
        self,
        handler
    ) -> "EngineBuilder":
        self.context.directive_registry.register(handler)
        return self


    def add_adapter(
        self,
        format_name: str,
        adapter
    ) -> "EngineBuilder":
        self.context.adapter_registry.register(
            format_name,
            adapter
        )
        return self


    def add_compiler(
        self,
        format_name: str,
        compiler
    ) -> "EngineBuilder":
        self.context.compiler_registry.register(
            format_name,
            compiler
        )
        return self

    def use_resource_resolver(self, resolver) -> "EngineBuilder":
        self.context.resource_resolver = resolver
        return self

    def use_runtime_resolver(self, resolver) -> "EngineBuilder":
        self.context.runtime_resolver = resolver
        return self

    def build(self):
        planning = PlanningModule(self.context)
        solving = SolvingModule(self.context)
        assembling = AssemblingModule(self.context)
        compilation = CompilationModule(self.context)

        return Engine(
            planning=planning,
            solving=solving,
            assembling=assembling,
            compilation=compilation,
        )

    @classmethod
    def default(cls):
        builder = cls()
        builder\
            .add_inspector(
                "md",
                MarkdownInspector()
            )\
            .add_directive(
                IncludeDirectiveHandler()
            )\
            .add_adapter(
                "md",
                MarkdownAdapter()
            )\
            .add_adapter(
                "pdf",
                PdfToImageMarkdownAdapter()
            )\
            .add_adapter(
                "docx",
                DocxAdapter()
            )\
            .add_adapter(
                "xlsx",
                ExcelToMarkdownAdapter()
            )\
            .add_adapter(
                "image",
                ImageMarkdownAdapter()
            )\
            .add_compiler(
                "docx",
                DocxCompiler()
            )\
            .add_compiler(
                "html",
                HtmlCompiler()
            )\
            .add_compiler(
                "pdf",
                PdfCompiler()
            )

        return builder