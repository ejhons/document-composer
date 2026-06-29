
import logging
import re
import os
import json
from typing import Dict, Any, Set
from jinja2 import Template
from engine.src.doc_engine.core.adapters import (
    AdapterRegistry, 
    ExcelToMarkdownAdapter,
    MermaidMarkdownAdapter, 
    PdfToImageMarkdownAdapter, 
    MarkdownPassthroughAdapter,
    DocxPostCompileAdapter
)
from engine.src.doc_engine.core.cache import CacheManager
from engine.src.doc_engine.core.compilers import(
    CompilerRegistry, 
    DocxCompilerAdapter, 
    PdfCompilerAdapter, 
    HtmlCompilerAdapter
)
from engine.src.doc_engine.core.models import ComponentConfig, RecipeManifest
from engine.src.doc_engine.core.parser import DocumentParser
from engine.src.doc_engine.core.sanitizers import DocumentSanitizers

logger = logging.getLogger("doc_engine.cache")

class DocumentEngine:
    def __init__(self,
                 manifest_path: str,
                 adapter_registry: AdapterRegistry | None = None,
                 compiler_registry: CompilerRegistry | None = None
                 ):
        with open(manifest_path, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)

        self.manifest = RecipeManifest(**raw_data)
        self.parser = DocumentParser()

        # Criação do ambiente Jinja2 customizado para suportar os filtros
        self.jinja_env = Template("").environment
        DocumentSanitizers.register_filters(self.jinja_env)

        # Inicializa o cache manager apontando para a pasta output raiz
        self.cache = CacheManager(cache_dir="engine/src/doc_engine/output")
        
        # 1. Initialize and boots-up the Registry Administrator layout
        self.registry = adapter_registry or AdapterRegistry()
        if adapter_registry is None:
            self._bootstrap_adapters()
        
        # 2. Initialize and boots-up the Output Exporter Registry
        self.compiler_registry = compiler_registry or CompilerRegistry()
        if compiler_registry is None:
            self._bootstrap_compilers()

    def _bootstrap_adapters(self):
        """Initializes default system plugins for file format resolution."""
        self.registry.register_adapter("xlsx", ExcelToMarkdownAdapter())
        self.registry.register_adapter("pdf", PdfToImageMarkdownAdapter())
        self.registry.register_adapter("md", MarkdownPassthroughAdapter())
        self.registry.register_adapter("docx", DocxPostCompileAdapter())

    def _bootstrap_compilers(self):
        """Initializes system plugins for compilation output formats."""
        self.compiler_registry.register_compiler("docx", DocxCompilerAdapter())
        self.compiler_registry.register_compiler("pdf", PdfCompilerAdapter())
        self.compiler_registry.register_compiler("html", HtmlCompilerAdapter())
        
    def should_render_component(self, component: ComponentConfig, user_inputs: Dict[str, Any]) -> bool:
        """Evaluates if a component condition statement resolves to True based on current user answers."""
        if not component.condition:
            return True # Sem condição significa que o bloco sempre entra
        
        try:
            # Cria um contexto limpo avaliando strings de forma segura
            # Exemplo de string: "has_parking == 'Sim'"
            # Passamos as variáveis digitadas pelo usuário como escopo de variáveis locais do eval()
            eval_scope = {k: str(v).strip() for k, v in user_inputs.items()}
            return bool(eval(component.condition, {"__builtins__": None}, eval_scope))
        except Exception as e:
            print(f"[Warning] Failed evaluating condition condition for block '{component.id}': {e}")
            return component.is_required # Fallback para o estado de obrigatoriedade do bloco
        
    def discover_required_fields(self) -> Dict[str, Dict[str, Any]]:
        """Scans all template components to build a unified catalog of input parameters."""
        consolidated_fields = {}
        
        for component in self.manifest.components:
            if component.type == "template":
                if not os.path.exists(component.source):
                    continue
                
                metadata, body = self.parser.parse_front_matter(component.source)
                variables = self.parser.extract_variables(body)
                fields_metadata = metadata.get("fields_definition", {})
                
                for var in variables:
                    if var not in consolidated_fields:
                        # Fallback definitions if not explicitly typed in YAML front matter
                        consolidated_fields[var] = fields_metadata.get(var, {
                            "data_type": "text",
                            "label": var.replace("_", " ").title(),
                            "source_component": component.id
                        })
        return consolidated_fields

    # Adicione este método dentro da classe DocumentEngine:
    def pre_process_markdown_diagrams(self, raw_markdown: str, output_resource_dir: str) -> str:
        """
        Scans the consolidated markdown string, extracts every ```mermaid block,
        converts it to a local PNG using the Mermaid adapter, and rewrites the content.
        """
        # Regex to capture content inside ```mermaid <content> ```
        mermaid_pattern = r'```mermaid\s*\n(.*?)\n```'
        
        matches = re.findall(mermaid_pattern, raw_markdown, re.DOTALL)
        if not matches:
            return raw_markdown

        processed_markdown = raw_markdown
        for index, diagram_code in enumerate(matches):
            diagram_id = f"mermaid_diagram_{index + 1}"
            # Define a unique name and path for each diagram image asset
            image_filename = f"rendered_diagram_{index + 1}.png"
            output_image_path = os.path.join(output_resource_dir, image_filename)
            
            # Process diagram text into image link using our adapter logic
            # image_markdown_tag = MermaidMarkdownAdapter.process_inline_diagram(
            #     diagram_code, output_image_path
            # )
            # 1. Calcula hash do texto do diagrama
            diagram_hash = self.cache.calculate_text_hash(diagram_code)
            
            # 2. Se o diagrama for idêntico e o PNG existir, pula a chamada da API
            if self.cache.is_cached(diagram_id, diagram_hash, [output_image_path]):
                logger.info(f"Cache hit for layout {diagram_id}. Reusing local PNG graphic structure.")
                image_markdown_tag = f"\n\n![System Diagram]({output_image_path})\n\n"
            else:
                # Cache miss: aciona a API externa via adaptador
                from engine.src.doc_engine.core.adapters import MermaidMarkdownAdapter
                image_markdown_tag = MermaidMarkdownAdapter.process_inline_diagram(
                    diagram_code, output_image_path
                )
                # Salva o novo estado no cache
                self.cache.update_cache(diagram_id, diagram_hash, [output_image_path])
            
            # Replace the code block with the new image tag in the final document text
            # We target the specific block to avoid accidental double replacements
            full_block_to_replace = f"```mermaid\n{diagram_code}\n```"
            processed_markdown = processed_markdown.replace(full_block_to_replace, image_markdown_tag)
            
        return processed_markdown

    def assemble_document(self, user_inputs: Dict[str, Any], output_resource_dir: str) -> str:
        """Processes dynamic blocks, handles placeholder values, and bundles text segments."""
        assembled_segments = []

        for component in self.manifest.components:
            # AVALIAÇÃO CONDICIONAL: Se a regra falhar, o bloco é completamente ignorado
            if not self.should_render_component(component, user_inputs):
                print(f"[Engine] Skipping conditional block: '{component.id}' (Condition check failed)")
                continue

            if component.type == "template":
                if not os.path.exists(component.source):
                    raise FileNotFoundError(f"Component file missing: {component.source}")
                
                _, body = self.parser.parse_front_matter(component.source)
                # Usamos o ambiente Jinja que possui nossos filtros registrados
                jinja_template = self.jinja_env.from_string(body)
                assembled_segments.append(jinja_template.render(user_inputs))
                # jinja_template = Template(body)
                # rendered_text = jinja_template.render(user_inputs)
                # assembled_segments.append(rendered_text)
                
            elif component.type == "external":
                if not os.path.exists(component.source):
                    print(f"[Warning] File asset path unavailable: {component.source}")
                    continue
                # 1. Calcula o fingerprint do arquivo externo antes de processá-lo
                file_hash = self.cache.calculate_file_hash(component.source)
                
                # Para arquivos como PDF, prevemos que a página 1 em PNG existirá se estiver cacheado
                base_name = os.path.splitext(os.path.basename(component.source))[0]
                sample_output = os.path.join(output_resource_dir, f"{base_name}_page_1.png")
                expected_files = [sample_output] if component.file_format == "pdf" else []

                # 2. Avalia hit do cache
                if self.cache.is_cached(component.id, file_hash, expected_files):
                    logger.info(f"Cache hit for external component '{component.id}'. Skipping adapter rendering step.")
                    # Arquivos markdown ou excel precisam ler os arquivos ou gerar strings de texto, 
                    # mas para fins do MVP focaremos o cache nos gargalos pesados: PDF e Imagens.
                    if component.file_format not in ["pdf", "image"]:
                        adapter = self.registry.get_adapter(component.file_format)
                        converted_content = adapter.convert(component.source, output_resource_dir)
                        assembled_segments.append(converted_content)
                        continue

                # Dynamic strategy execution - pure polymorphic call
                # Engine doesn't know HOW it translates, it just triggers the Port contract
                adapter = self.registry.get_adapter(component.file_format)
                converted_content = adapter.convert(component.source, output_resource_dir)
                assembled_segments.append(converted_content)

                # Static entry marker placeholder for downstream native compiler binding
                # assembled_segments.append(f"\n\n<!-- ATTACH EXTERNAL FILE: {component.source} -->\n\n")
                
                # 3. Registra ou atualiza o cache pós execução de sucesso
                self.cache.update_cache(component.id, file_hash, [sample_output])

        return "\n\n".join(assembled_segments)