from typing import Any, Optional
from abc import ABC, abstractmethod
from engine.src.doc_engine.models.recipe import RecipeManifest

# =====================================================================
# 1. THE OUTPUT PORT (Abstract Base Class)
# =====================================================================
class BaseCompilerAdapter(ABC):
    """
    The Output Port contract for document generation.
    Every format exporter (Docx, Pdf, Html) must satisfy this interface.
    """
    def __init__(
            self,
            registry: Optional[Any] = None
        ):
        # Recebe a injeção do registro de adaptadores se necessário
        self.registry = registry

    @abstractmethod
    def compile(
        self, 
        source_markdown_path: str,
        output_path: str,
        manifest: RecipeManifest,
        **kwargs
    ) -> str:
        """Translates the compiled Markdown into the target binary format layout."""
        pass


































# =====================================================================
# 2. FORMAT-SPECIFIC EXPORTER ADAPTERS
# # =====================================================================
# class DocxCompilerAdapter(BaseCompilerAdapter):
#     def compile(
#             self, 
#             source_markdown_path: str,
#             output_path: str, 
#             manifest: RecipeManifest,
#             **kwargs
#         ) -> str:
#         # 1. Executa a compilação padrão do Pandoc
#         extra_args = ["--webtex"]
#         reference_path = manifest.style.reference_docx
#         if reference_path and os.path.exists(reference_path):
#             extra_args.append(f"--reference-doc={reference_path}")
#         else:
#             print(f"[Style Warning] reference.docx não configurado. Para cabeçalhos nativos no Word, forneça um arquivo base estilizado.")

#         pypandoc.convert_file(
#             source_file=source_markdown_path,
#             to="docx",
#             outputfile=output_path,
#             extra_args=extra_args
#         )

#         # # 2. COMPORTAMENTO ENCAPSULADO (Refatoração):
#         # # O próprio adaptador agora assume o pós-processamento exclusivo do ecossistema Word.
#         # # Importamos a engine de forma tardia (lazy import) para evitar importações cíclicas se necessário.
#         # from engine.src.doc_engine.core.engine import DocumentEngine
        
#         # # Como precisamos do registro de adaptadores de entrada para mesclar os binários do docx,
#         # # instanciamos um escopo temporário ou passamos a lógica diretamente.
#         # print("[Compiler - DOCX] Initiating post-compile subdocument binary structural binding merge...")
        
#         # # Criamos uma instância leve do leitor para recuperar o adaptador de merge do docx
#         # # (Ou podemos acessar o registro global se preferir, mas essa abordagem isola o comportamento)
#         # from engine.src.doc_engine.core.registry import AdapterRegistry
#         # registry = AdapterRegistry()
#         # from engine.src.doc_engine.core.adapters import DocxMarkdownAdapter
#         # registry.register_adapter("docx", DocxMarkdownAdapter())
        
#         # docx_input_adapter = registry.get_adapter("docx")
        
#         if self.registry:
#             try:
#                 docx_input_adapter = self.registry.get_adapter("docx")                
#                 for component in manifest.components:
#                     if component.type == "external" and component.file_format == "docx":
#                         if os.path.exists(component.source):
#                             print(f"[Compiler - DOCX] Merging physical component via injected adapter: {component.source}")
#                             docx_input_adapter.execute_binary_merge(output_path, component.source)
#             except ValueError:
#                 print("[Compiler - DOCX Warning] Input adapter for 'docx' merge not found in injected registry.")
                
#         return output_path


# class PdfCompilerAdapter(BaseCompilerAdapter):
#     def compile(
#             self,
#             source_markdown_path: str,
#             output_path: str,
#             manifest: RecipeManifest,
#             **kwargs
#         ) -> str:
#         """
#         Compiles Markdown to PDF by leveraging the existing HTML pipeline,
#         ensuring perfect layout control via CSS.
#         """
#         # 1. Definimos um caminho temporário para o HTML intermediário estilizado
#         temp_html_path = output_path.replace(".pdf", "_interim.html")
#         temp_template_path = output_path.replace(".pdf", "_template.html")
#         style = manifest.style
        
#          # 3. CONSTRUÇÃO DO DOCUMENTO COMPATÍVEL:
#         # Criamos uma folha de estilo ultra-restrita usando apenas o que o xhtml2pdf entende perfeitamente
#         safe_css = (
#             f"<style>"
#             f"@page {{ size: a4; margin: 2.5cm; }}"
#             f"body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333333; line-height: 1.5; }}"
#             f"h1 {{ font-size: 22pt; color: {style.primary_color}; border-bottom: 0.5pt solid {style.primary_color}; padding-bottom: 3px; }}"
#             f"h2 {{ font-size: 16pt; color: {style.primary_color}; margin-top: 15px; }}"
#             f"h3 {{ font-size: 13pt; color: {style.primary_color}; }}"
#             f"table {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}"
#             f"th {{ background-color: {style.primary_color}; color: #ffffff; padding: 6px; text-align: left; font-size: 10pt; }}"
#             f"td {{ border: 0.5pt solid #dddddd; padding: 6px; font-size: 10pt; }}"
#             f"img {{ max-width: 100%; height: auto; }}"
#             f"</style>"
#         )

#         custom_html_template = (
#             "<!DOCTYPE html>\n"
#             "<html>\n"
#             "<head>\n"
#             "  <meta charset='utf-8' />\n"
#             f"{safe_css}"
#             "</head>\n"
#             "<body>\n"
#             "$body$\n" # Variável interna do Pandoc onde ele despeja as tags limpas
#             "</body>\n"
#             "</html>"
#         )

#         # 2. Instanciamos e reaproveitamos o adaptador de HTML já existente
#         # Isso garante que TODO o CSS, cabeçalhos e rodapés gerados lá sejam herdados aqui
#         html_compiler = HtmlCompilerAdapter()
#         # html_compiler.compile(source_markdown_path, temp_html_path, manifest)
#         html_compiler.compile(source_markdown_path, temp_html_path, manifest, standalone=False)
#         # print(f"[Compiler - PDF] Compiling final vector PDF directly from styled HTML blueprint...")
#         print(f"[Compiler - PDF Native] Converting cleaned HTML template to vector PDF via xhtml2pdf...")
        
#         try:
#             # Salva o template no disco temporariamente
#             with open(temp_template_path, "w", encoding="utf-8") as tpl_file:
#                 tpl_file.write(custom_html_template)
#             # 2. Compilação do Pandoc OBRIGANDO o uso do nosso template
#             pypandoc.convert_file(
#                 source_file=source_markdown_path,
#                 to="html5",
#                 outputfile=temp_html_path,
#                 extra_args=[
#                     "--webtex", 
#                     "-V", "lang=pt-BR",
#                     f"--template={temp_template_path}" # A mágica acontece aqui!
#                 ]
#             )

#             with open(temp_html_path, "r", encoding="utf-8") as html_file:
#                 raw_html_body = html_file.read()
            
#             # 2. SANITIZAÇÃO AGRESSIVA VIA REGEX:
#             # Remove absolutamente QUALQUER tag <style>...</style> que o Pandoc tenha enfiado de intruso
#             clean_html_body = re.sub(r'<style[^>]*>.*?</style>', '', raw_html_body, flags=re.DOTALL)
            
           
            
#             # Montamos a estrutura final envelopada
#             final_sanitized_html = (
#                 f"<!DOCTYPE html>"
#                 f"<html>"
#                 f"<head><meta charset='utf-8'>{safe_css}</head>"
#                 f"<body>{clean_html_body}</body>"
#                 f"</html>"
#             )
#             # 3. Lemos o HTML perfeitamente limpo
#             with open(temp_html_path, "r", encoding="utf-8") as html_file:
#                 final_sanitized_html = html_file.read()
            
#             # 4. Geração Nativa do PDF
#             with open(output_path, "wb") as pdf_file:
#                 pisa_status = pisa.CreatePDF(src=final_sanitized_html, dest=pdf_file)
                
#             if pisa_status.err:
#                 print(f"[Compiler - PDF Warning] xhtml2pdf processing finalized with minor warnings.")
                
#         finally:
#             # Limpeza cirúrgica dos temporários
#             if os.path.exists(temp_html_path):
#                 os.remove(temp_html_path)
#             if os.path.exists(temp_template_path):
#                 os.remove(temp_template_path)
                
#         return output_path

# class HtmlCompilerAdapter(BaseCompilerAdapter):
#     def compile(self, source_markdown_path: str, output_path: str, manifest: RecipeManifest, **kwargs) -> str:
#         standalone = kwargs.get('standalone', True)
#         """Standard compilation for browser consumption."""
#         return self._execute_pypandoc_html(source_markdown_path, output_path, manifest, standalone=standalone)
    
#     # def compile(self, source_markdown_path: str, output_path: str, manifest: RecipeManifest) -> str:
#     def _execute_pypandoc_html(self, source_markdown_path: str, output_path: str, manifest: RecipeManifest, standalone: bool) -> str:
#         style = manifest.style
#         # CSS puro e simples aceito pelo xhtml2pdf e navegadores
#         css_content = (
#             f"<style>"
#             f"body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333333; line-height: 1.5; }}"
#             f"h1, h2, h3, h4 {{ color: {style.primary_color}; font-family: Helvetica, Arial, sans-serif; }}"
#             f"h1 {{ font-size: 20pt; border-bottom: 1px solid {style.primary_color}; padding-bottom: 5px; }}"
#             f"h2 {{ font-size: 16pt; margin-top: 20px; }}"
#             f"table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}"
#             f"th {{ background-color: {style.primary_color}; color: white; padding: 8px; text-align: left; font-size: 10pt; }}"
#             f"td {{ border: 1px solid #dddddd; padding: 8px; font-size: 10pt; }}"
#             f"img {{ max-width: 100%; height: auto; }}"
#             f"</style>"
#         )

#         # 1. Criamos um bloco CSS inline customizado com base nas cores do Manifesto
#         # css_header_footer = (
#         #     f"<style>"
#         #     f"body {{ font-family: Arial, sans-serif; margin: 50px auto; max-width: 800px; color: #333; line-height: 1.6; }}"
#         #     f".doc-header {{ display: flex; justify-content: space-between; border-bottom: 2px solid {style.primary_color}; padding-bottom: 10px; margin-bottom: 30px; font-size: 12px; color: #666; }}"
#         #     f".doc-footer {{ border-top: 1px solid #ccc; margin-top: 50px; padding-top: 10px; display: flex; justify-content: space-between; font-size: 11px; color: #888; }}"
#         #     f"h1, h2, h3 {{ color: {style.primary_color}; }}"
#         #     f"</style>"
#         # )
#         # Argumentos para HTML profissional:
#         # --standalone (-s): Gera um documento HTML completo com <head>, <body> e estilos CSS básicos, em vez de apenas um fragmento de texto.
#         # --mathjax: Garante que as equações LaTeX sejam renderizadas com perfeição e interatividade matemática direto no navegador.
#         # extra_args = [
#         #     "--standalone",
#         #     "--mathjax",
#         #     "-V", "lang=pt-BR",
#         #     "--metadata", f"title={manifest.recipe_name}"
#         # ]
#         extra_args = [
#             "--webtex",
#             "-V", "lang=pt-BR"
#         ]
# # Ativa o modo autônomo do Pandoc apenas se não formos enviar para o xhtml2pdf
#         print('standalone', standalone)
#         if standalone:
#             extra_args.append("--standalone")
#             extra_args.append("--mathjax")
#             extra_args.append(f"--metadata=title:{manifest.recipe_name}")

#         # Injeção básica de elementos estruturais
#         # Para evitar problemas com paths, escrevemos o fragmento de estilo diretamente
#         if style.include_header:
#             header_html = (
#                 f"{css_content}"
#                 f"<div style='display:block; border-bottom: 1px solid #ccc; font-size: 9pt; color: #666; margin-bottom: 20px;'>"
#                 f"<span>{style.header_text_left}</span>"
#                 f"<span>{style.header_text_right or manifest.recipe_name}</span>"
#                 f"</div>"
#             )
#             with open("engine/src/doc_engine/output_temp_header.html", "w", encoding="utf-8") as f:
#                 f.write(header_html)
#             extra_args.append("--include-before-body=engine/src/doc_engine/output_temp_header.html")

#         # 3. Injetamos o rodapé na base (include-after-body) se ativo no manifesto
#         if style.include_footer:
#             footer_html = (
#                 f"<div class='doc-footer'>"
#                 f"<span>{style.footer_text_left}</span>"
#                 f"<span>Gerado Automaticamente - DocComposer v{manifest.version}</span>"
#                 f"</div>"
#             )
#             with open("engine/src/doc_engine/output/temp_footer.html", "w", encoding="utf-8") as f:
#                 f.write(footer_html)
#             extra_args.append("--include-after-body=engine/src/doc_engine/output/temp_footer.html")
        
#         # # 2. Injetamos o cabeçalho no topo (include-before-body) se ativo no manifesto
#         # if style.include_header:
#         #     header_html = (
#         #         f"{css_header_footer}"
#         #         f"<div class='doc-header'>"
#         #         f"<span>{style.header_text_left}</span>"
#         #         f"<span>{style.header_text_right or manifest.recipe_name}</span>"
#         #         f"</div>"
#         #     )
#         #     # Salvamos um fragmento temporário para o Pandoc embutir
#         #     with open("engine/src/doc_engine/output/temp_header.html", "w", encoding="utf-8") as f:
#         #         f.write(header_html)
#         #     extra_args.append("--include-before-body=engine/src/doc_engine/output/temp_header.html")

#         # 3. Injetamos o rodapé na base (include-after-body) se ativo no manifesto
#         # if style.include_footer:
#         #     footer_html = (
#         #         f"<div class='doc-footer'>"
#         #         f"<span>{style.footer_text_left}</span>"
#         #         f"<span>Gerado Automaticamente - DocComposer v{manifest.version}</span>"
#         #         f"</div>"
#         #     )
#         #     with open("engine/src/doc_engine/output/temp_footer.html", "w", encoding="utf-8") as f:
#         #         f.write(footer_html)
#         #     extra_args.append("--include-after-body=engine/src/doc_engine/output/temp_footer.html")
#         pypandoc.convert_file(
#             source_file=source_markdown_path,
#             to="html5",
#             outputfile=output_path,
#             extra_args=extra_args
#         )

#         # Limpeza de resíduos temporários de build
#         for temp_file in ["engine/src/doc_engine/output/temp_header.html", "engine/src/doc_engine/output/temp_footer.html"]:
#             if os.path.exists(temp_file):
#                 os.remove(temp_file)

#         return output_path

