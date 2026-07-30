import os
import re
import pypandoc

from pathlib import Path
from xhtml2pdf import pisa

from engine.compilation.compilers.base import BaseCompiler
from engine.runtime.execution.session import ExecutionSession



class PdfCompiler(BaseCompiler):        
    def compile(
        self,
        session: ExecutionSession,
        source_markdown_path: str,
        output_path: str,
        **kwargs
    ) -> str:       
        # if not self.registry: 
        #     print("[Compiler - DOCX Warning] Input adapter for 'docx' merge not found in injected registry.")
        temp_html_path = None
        temp_template_path = None
        try:
            obj = self._create_temp_html(
                session=session,
                source_markdown_path=source_markdown_path,
                output_pdf_path=output_path
            )
            temp_html_path = obj.get("temp_html_path")
            temp_template_path = obj.get("temp_template_path")
            final_sanitized_html = obj.get("final_sanitized_html")

            path = self._execute_pypandoc_pdf(
                final_sanitized_html=final_sanitized_html,
                output_path=output_path
            )
        
        finally:
            # Limpeza cirúrgica dos temporários
            if temp_html_path and os.path.exists(temp_html_path):
                os.remove(temp_html_path)
            if temp_template_path and os.path.exists(temp_template_path):
                os.remove(temp_template_path)
                
        return Path(path)

    #==========================
    #  
    #==========================
    def _create_temp_html(
        self,
        session: ExecutionSession,
        source_markdown_path: str,
        output_pdf_path: str
    ) -> dict[str, str]:
        """
        Compiles Markdown to PDF by leveraging the existing HTML pipeline,
        ensuring perfect layout control via CSS.
        """
        manifest = session.manifest
        # 1. Definimos um caminho temporário para o HTML intermediário estilizado
        temp_html_path = output_pdf_path.replace(".pdf", "_interim.html")
        temp_template_path = output_pdf_path.replace(".pdf", "_template.html")
        style = manifest.style
        
        # 3. CONSTRUÇÃO DO DOCUMENTO COMPATÍVEL:
        # Criamos uma folha de estilo ultra-restrita usando apenas o que o xhtml2pdf entende perfeitamente
        safe_css = (
            f"<style>"
            f"@page {{ size: a4; margin: 2.5cm; }}"
            f"body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333333; line-height: 1.5; }}"
            f"h1 {{ font-size: 22pt; color: {style.primary_color}; border-bottom: 0.5pt solid {style.primary_color}; padding-bottom: 3px; }}"
            f"h2 {{ font-size: 16pt; color: {style.primary_color}; margin-top: 15px; }}"
            f"h3 {{ font-size: 13pt; color: {style.primary_color}; }}"
            f"table {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}"
            f"th {{ background-color: {style.primary_color}; color: #ffffff; padding: 6px; text-align: left; font-size: 10pt; }}"
            f"td {{ border: 0.5pt solid #dddddd; padding: 6px; font-size: 10pt; }}"
            f"img {{ max-width: 100%; height: auto; }}"
            f"</style>"
        )

        custom_html_template = (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            "  <meta charset='utf-8' />\n"
            f"{safe_css}"
            "</head>\n"
            "<body>\n"
            "$body$\n" # Variável interna do Pandoc onde ele despeja as tags limpas
            "</body>\n"
            "</html>"
        )

        # 2. Instanciamos e reaproveitamos o adaptador de HTML já existente
        # Isso garante que TODO o CSS, cabeçalhos e rodapés gerados lá sejam herdados aqui
        html_compiler = self.registry.get('html')
        html_compiler.compile(
            session=session,
            source_markdown_path=source_markdown_path,
            output_path=temp_html_path,
            standalone=False
        )
        # print(f"[Compiler - PDF] Compiling final vector PDF directly from styled HTML blueprint...")
        print(f"[Compiler - PDF Native] Converting cleaned HTML template to vector PDF via xhtml2pdf...")
        
        # try:
        # Salva o template no disco temporariamente
        with open(temp_template_path, "w", encoding="utf-8") as tpl_file:
            tpl_file.write(custom_html_template)
        # 2. Compilação do Pandoc OBRIGANDO o uso do nosso template
        pypandoc.convert_file(
            source_file=source_markdown_path,
            to="html5",
            outputfile=temp_html_path,
            extra_args=[
                "--webtex", 
                "-V", "lang=pt-BR",
                f"--template={temp_template_path}" # A mágica acontece aqui!
            ]
        )

        with open(temp_html_path, "r", encoding="utf-8") as html_file:
            raw_html_body = html_file.read()
        
        # 2. SANITIZAÇÃO AGRESSIVA VIA REGEX:
        # Remove absolutamente QUALQUER tag <style>...</style> que o Pandoc tenha enfiado de intruso
        clean_html_body = re.sub(r'<style[^>]*>.*?</style>', '', raw_html_body, flags=re.DOTALL)
        
        # Montamos a estrutura final envelopada
        final_sanitized_html = (
            f"<!DOCTYPE html>"
            f"<html>"
            f"<head><meta charset='utf-8'>{safe_css}</head>"
            f"<body>{clean_html_body}</body>"
            f"</html>"
        )
        #     # 3. Lemos o HTML perfeitamente limpo
        #     with open(temp_html_path, "r", encoding="utf-8") as html_file:
        #         final_sanitized_html = html_file.read()

        return {
            "final_sanitized_html":final_sanitized_html,
            "temp_template_path":temp_template_path,
            "temp_html_path":temp_html_path
        }



    def _execute_pypandoc_pdf(
        self,
        final_sanitized_html: str,
        output_path: str,
    ) -> str:
        # 4. Geração Nativa do PDF
        with open(output_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(src=final_sanitized_html, dest=pdf_file)
            
        if pisa_status.err:
            print(f"[Compiler - PDF Warning] xhtml2pdf processing finalized with minor warnings.")
                
        return output_path

    # def _execute_pypandoc_pdf(
    #     self,
    #     source_markdown_path: str,
    #     output_path: str,
    #     manifest: RecipeManifest
    # ) -> str:
    #     """
    #     Compiles Markdown to PDF by leveraging the existing HTML pipeline,
    #     ensuring perfect layout control via CSS.
    #     """
    #     # 1. Definimos um caminho temporário para o HTML intermediário estilizado
    #     temp_html_path = output_path.replace(".pdf", "_interim.html")
    #     temp_template_path = output_path.replace(".pdf", "_template.html")
    #     style = manifest.style
        
    #      # 3. CONSTRUÇÃO DO DOCUMENTO COMPATÍVEL:
    #     # Criamos uma folha de estilo ultra-restrita usando apenas o que o xhtml2pdf entende perfeitamente
    #     safe_css = (
    #         f"<style>"
    #         f"@page {{ size: a4; margin: 2.5cm; }}"
    #         f"body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333333; line-height: 1.5; }}"
    #         f"h1 {{ font-size: 22pt; color: {style.primary_color}; border-bottom: 0.5pt solid {style.primary_color}; padding-bottom: 3px; }}"
    #         f"h2 {{ font-size: 16pt; color: {style.primary_color}; margin-top: 15px; }}"
    #         f"h3 {{ font-size: 13pt; color: {style.primary_color}; }}"
    #         f"table {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}"
    #         f"th {{ background-color: {style.primary_color}; color: #ffffff; padding: 6px; text-align: left; font-size: 10pt; }}"
    #         f"td {{ border: 0.5pt solid #dddddd; padding: 6px; font-size: 10pt; }}"
    #         f"img {{ max-width: 100%; height: auto; }}"
    #         f"</style>"
    #     )

    #     custom_html_template = (
    #         "<!DOCTYPE html>\n"
    #         "<html>\n"
    #         "<head>\n"
    #         "  <meta charset='utf-8' />\n"
    #         f"{safe_css}"
    #         "</head>\n"
    #         "<body>\n"
    #         "$body$\n" # Variável interna do Pandoc onde ele despeja as tags limpas
    #         "</body>\n"
    #         "</html>"
    #     )

    #     # 2. Instanciamos e reaproveitamos o adaptador de HTML já existente
    #     # Isso garante que TODO o CSS, cabeçalhos e rodapés gerados lá sejam herdados aqui
    #     # html_compiler = HtmlCompiler()
    #     # html_compiler.compile(source_markdown_path, temp_html_path, manifest)
    #     html_compiler = self.registry.get('html')
    #     html_compiler.compile(
    #         source_markdown_path,
    #         temp_html_path,
    #         manifest,
    #         standalone=False
    #     )
    #     # print(f"[Compiler - PDF] Compiling final vector PDF directly from styled HTML blueprint...")
    #     print(f"[Compiler - PDF Native] Converting cleaned HTML template to vector PDF via xhtml2pdf...")
        
    #     try:
    #         # Salva o template no disco temporariamente
    #         with open(temp_template_path, "w", encoding="utf-8") as tpl_file:
    #             tpl_file.write(custom_html_template)
    #         # 2. Compilação do Pandoc OBRIGANDO o uso do nosso template
    #         pypandoc.convert_file(
    #             source_file=source_markdown_path,
    #             to="html5",
    #             outputfile=temp_html_path,
    #             extra_args=[
    #                 "--webtex", 
    #                 "-V", "lang=pt-BR",
    #                 f"--template={temp_template_path}" # A mágica acontece aqui!
    #             ]
    #         )

    #         with open(temp_html_path, "r", encoding="utf-8") as html_file:
    #             raw_html_body = html_file.read()
            
    #         # 2. SANITIZAÇÃO AGRESSIVA VIA REGEX:
    #         # Remove absolutamente QUALQUER tag <style>...</style> que o Pandoc tenha enfiado de intruso
    #         clean_html_body = re.sub(r'<style[^>]*>.*?</style>', '', raw_html_body, flags=re.DOTALL)
            
    #         # Montamos a estrutura final envelopada
    #         final_sanitized_html = (
    #             f"<!DOCTYPE html>"
    #             f"<html>"
    #             f"<head><meta charset='utf-8'>{safe_css}</head>"
    #             f"<body>{clean_html_body}</body>"
    #             f"</html>"
    #         )
    #         # 3. Lemos o HTML perfeitamente limpo
    #         with open(temp_html_path, "r", encoding="utf-8") as html_file:
    #             final_sanitized_html = html_file.read()
            
    #         # 4. Geração Nativa do PDF
    #         with open(output_path, "wb") as pdf_file:
    #             pisa_status = pisa.CreatePDF(src=final_sanitized_html, dest=pdf_file)
                
    #         if pisa_status.err:
    #             print(f"[Compiler - PDF Warning] xhtml2pdf processing finalized with minor warnings.")
                
    #     finally:
    #         # Limpeza cirúrgica dos temporários
    #         if os.path.exists(temp_html_path):
    #             os.remove(temp_html_path)
    #         if os.path.exists(temp_template_path):
    #             os.remove(temp_template_path)
                
    #     return output_path