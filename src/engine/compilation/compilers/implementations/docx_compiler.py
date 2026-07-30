import os
import pypandoc
from pathlib import Path
from docx import Document
from engine.frontend.manifests.recipe import RecipeManifest
from engine.compilation.compilers.base import BaseCompiler
from engine.frontend.syntax.markdown.atomized_markdown import AtomizedMarkdown
from engine.runtime.execution.session import ExecutionSession


class DocxCompiler(BaseCompiler):
    def compile(
        self,
        session: ExecutionSession,
        source_markdown_path: str,
        output_path: str,
    ) -> str:       
        # if not self.registry: 
        #     print("[Compiler - DOCX Warning] Input adapter for 'docx' merge not found in injected registry.")
    
        path = self._execute_pypandoc_docx(
            source_markdown_path=source_markdown_path,
            output_path=output_path,
            manifest=session.manifest
        )
        return Path(path)

    
    def _execute_pypandoc_docx(
            self,
            source_markdown_path: str,
            output_path: str,
            manifest: RecipeManifest
        ) -> str:
        # 1. Executa a compilação padrão do Pandoc
        extra_args = ["--webtex"]
        reference_path = manifest.style.reference_docx

        if reference_path and os.path.exists(reference_path):
            extra_args.append(f"--reference-doc={reference_path}")
        else:
            print(f"[Style Warning] reference.docx não configurado. Para cabeçalhos nativos no Word, forneça um arquivo base estilizado.")

        pypandoc.convert_file(
            source_file=source_markdown_path,
            to="docx",
            outputfile=output_path,
            extra_args=extra_args
        )

        
        # if self.registry:
        #     try:
        #         docx_input_adapter = self.registry.get_adapter("docx")                
        #         for component in manifest.components:
        #             if component.type == "external" and component.file_format == "docx":
        #                 if os.path.exists(component.source):
        #                     print(f"[Compiler - DOCX] Merging physical component via injected adapter: {component.source}")
        #                     self._execute_binary_merge(output_path, component.source)
        #     except ValueError:
        #         print("[Compiler - DOCX Warning] Input adapter for 'docx' merge not found in injected registry.")
                
        return output_path


    def _execute_binary_merge(
        self,
        master_docx_path: str,
        external_docx_path: str
    ):
        """Specialized secondary action for docx post-processing layer."""
        if not os.path.exists(master_docx_path) or not os.path.exists(external_docx_path):
            raise FileNotFoundError("Missing target binaries for structural append.")
        
        master_doc = Document(master_docx_path)
        external_doc = Document(external_docx_path)
        master_doc.add_page_break()
        
        for element in external_doc.element.body:
            master_doc.element.body.append(element)
            
        master_doc.save(master_docx_path)


        # # 2. COMPORTAMENTO ENCAPSULADO (Refatoração):
        # # O próprio adaptador agora assume o pós-processamento exclusivo do ecossistema Word.
        # # Importamos a engine de forma tardia (lazy import) para evitar importações cíclicas se necessário.
        # from engine.src.doc_engine.core.engine import DocumentEngine
        
        # # Como precisamos do registro de adaptadores de entrada para mesclar os binários do docx,
        # # instanciamos um escopo temporário ou passamos a lógica diretamente.
        # print("[Compiler - DOCX] Initiating post-compile subdocument binary structural binding merge...")
        
        # # Criamos uma instância leve do leitor para recuperar o adaptador de merge do docx
        # # (Ou podemos acessar o registro global se preferir, mas essa abordagem isola o comportamento)
        # from engine.src.doc_engine.core.registry import AdapterRegistry
        # registry = AdapterRegistry()
        # from engine.src.doc_engine.core.adapters import DocxMarkdownAdapter
        # registry.register_adapter("docx", DocxMarkdownAdapter())
        
        # docx_input_adapter = registry.get_adapter("docx")