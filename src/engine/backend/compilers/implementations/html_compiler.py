import os
import pypandoc
from engine.common.models.recipe import RecipeManifest
from engine.backend.compilers.base import BaseCompilerAdapter

class HtmlCompilerAdapter(BaseCompilerAdapter):
    def compile(self, source_markdown_path: str, output_path: str, manifest: RecipeManifest, **kwargs) -> str:
        standalone = kwargs.get('standalone', True)
        """Standard compilation for browser consumption."""
        return self._execute_pypandoc_html(source_markdown_path, output_path, manifest, standalone=standalone)
    
    # def compile(self, source_markdown_path: str, output_path: str, manifest: RecipeManifest) -> str:
    def _execute_pypandoc_html(self, source_markdown_path: str, output_path: str, manifest: RecipeManifest, standalone: bool) -> str:
        style = manifest.style
        # CSS puro e simples aceito pelo xhtml2pdf e navegadores
        css_content = (
            f"<style>"
            f"body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333333; line-height: 1.5; }}"
            f"h1, h2, h3, h4 {{ color: {style.primary_color}; font-family: Helvetica, Arial, sans-serif; }}"
            f"h1 {{ font-size: 20pt; border-bottom: 1px solid {style.primary_color}; padding-bottom: 5px; }}"
            f"h2 {{ font-size: 16pt; margin-top: 20px; }}"
            f"table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}"
            f"th {{ background-color: {style.primary_color}; color: white; padding: 8px; text-align: left; font-size: 10pt; }}"
            f"td {{ border: 1px solid #dddddd; padding: 8px; font-size: 10pt; }}"
            f"img {{ max-width: 100%; height: auto; }}"
            f"</style>"
        )

        # 1. Criamos um bloco CSS inline customizado com base nas cores do Manifesto
        # css_header_footer = (
        #     f"<style>"
        #     f"body {{ font-family: Arial, sans-serif; margin: 50px auto; max-width: 800px; color: #333; line-height: 1.6; }}"
        #     f".doc-header {{ display: flex; justify-content: space-between; border-bottom: 2px solid {style.primary_color}; padding-bottom: 10px; margin-bottom: 30px; font-size: 12px; color: #666; }}"
        #     f".doc-footer {{ border-top: 1px solid #ccc; margin-top: 50px; padding-top: 10px; display: flex; justify-content: space-between; font-size: 11px; color: #888; }}"
        #     f"h1, h2, h3 {{ color: {style.primary_color}; }}"
        #     f"</style>"
        # )
        # Argumentos para HTML profissional:
        # --standalone (-s): Gera um documento HTML completo com <head>, <body> e estilos CSS básicos, em vez de apenas um fragmento de texto.
        # --mathjax: Garante que as equações LaTeX sejam renderizadas com perfeição e interatividade matemática direto no navegador.
        # extra_args = [
        #     "--standalone",
        #     "--mathjax",
        #     "-V", "lang=pt-BR",
        #     "--metadata", f"title={manifest.recipe_name}"
        # ]
        extra_args = [
            "--webtex",
            "-V", "lang=pt-BR"
        ]
# Ativa o modo autônomo do Pandoc apenas se não formos enviar para o xhtml2pdf
        print('standalone', standalone)
        if standalone:
            extra_args.append("--standalone")
            extra_args.append("--mathjax")
            extra_args.append(f"--metadata=title:{manifest.recipe_name}")

        # Injeção básica de elementos estruturais
        # Para evitar problemas com paths, escrevemos o fragmento de estilo diretamente
        if style.include_header:
            header_html = (
                f"{css_content}"
                f"<div style='display:block; border-bottom: 1px solid #ccc; font-size: 9pt; color: #666; margin-bottom: 20px;'>"
                f"<span>{style.header_text_left}</span>"
                f"<span>{style.header_text_right or manifest.recipe_name}</span>"
                f"</div>"
            )
            with open("engine/src/doc_engine/output_temp_header.html", "w", encoding="utf-8") as f:
                f.write(header_html)
            extra_args.append("--include-before-body=engine/src/doc_engine/output_temp_header.html")

        # 3. Injetamos o rodapé na base (include-after-body) se ativo no manifesto
        if style.include_footer:
            footer_html = (
                f"<div class='doc-footer'>"
                f"<span>{style.footer_text_left}</span>"
                f"<span>Gerado Automaticamente - DocComposer v{manifest.version}</span>"
                f"</div>"
            )
            with open("engine/src/doc_engine/output/temp_footer.html", "w", encoding="utf-8") as f:
                f.write(footer_html)
            extra_args.append("--include-after-body=engine/src/doc_engine/output/temp_footer.html")
        
        # # 2. Injetamos o cabeçalho no topo (include-before-body) se ativo no manifesto
        # if style.include_header:
        #     header_html = (
        #         f"{css_header_footer}"
        #         f"<div class='doc-header'>"
        #         f"<span>{style.header_text_left}</span>"
        #         f"<span>{style.header_text_right or manifest.recipe_name}</span>"
        #         f"</div>"
        #     )
        #     # Salvamos um fragmento temporário para o Pandoc embutir
        #     with open("engine/src/doc_engine/output/temp_header.html", "w", encoding="utf-8") as f:
        #         f.write(header_html)
        #     extra_args.append("--include-before-body=engine/src/doc_engine/output/temp_header.html")

        # 3. Injetamos o rodapé na base (include-after-body) se ativo no manifesto
        # if style.include_footer:
        #     footer_html = (
        #         f"<div class='doc-footer'>"
        #         f"<span>{style.footer_text_left}</span>"
        #         f"<span>Gerado Automaticamente - DocComposer v{manifest.version}</span>"
        #         f"</div>"
        #     )
        #     with open("engine/src/doc_engine/output/temp_footer.html", "w", encoding="utf-8") as f:
        #         f.write(footer_html)
        #     extra_args.append("--include-after-body=engine/src/doc_engine/output/temp_footer.html")
        pypandoc.convert_file(
            source_file=source_markdown_path,
            to="html5",
            outputfile=output_path,
            extra_args=extra_args
        )

        # Limpeza de resíduos temporários de build
        for temp_file in ["engine/src/doc_engine/output/temp_header.html", "engine/src/doc_engine/output/temp_footer.html"]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        return output_path


class HtmlCompilerAdapter(BaseCompilerAdapter):
    def compile(self, source_markdown_path: str, output_path: str, manifest: RecipeManifest, **kwargs) -> str:
        standalone = kwargs.get('standalone', True)
        """Standard compilation for browser consumption."""
        return self._execute_pypandoc_html(source_markdown_path, output_path, manifest, standalone=standalone)
    
    # def compile(self, source_markdown_path: str, output_path: str, manifest: RecipeManifest) -> str:
    def _execute_pypandoc_html(self, source_markdown_path: str, output_path: str, manifest: RecipeManifest, standalone: bool) -> str:
        style = manifest.style
        # CSS puro e simples aceito pelo xhtml2pdf e navegadores
        css_content = (
            f"<style>"
            f"body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333333; line-height: 1.5; }}"
            f"h1, h2, h3, h4 {{ color: {style.primary_color}; font-family: Helvetica, Arial, sans-serif; }}"
            f"h1 {{ font-size: 20pt; border-bottom: 1px solid {style.primary_color}; padding-bottom: 5px; }}"
            f"h2 {{ font-size: 16pt; margin-top: 20px; }}"
            f"table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}"
            f"th {{ background-color: {style.primary_color}; color: white; padding: 8px; text-align: left; font-size: 10pt; }}"
            f"td {{ border: 1px solid #dddddd; padding: 8px; font-size: 10pt; }}"
            f"img {{ max-width: 100%; height: auto; }}"
            f"</style>"
        )
        extra_args = [
            "--webtex",
            "-V", "lang=pt-BR"
        ]
# Ativa o modo autônomo do Pandoc apenas se não formos enviar para o xhtml2pdf
        print('standalone', standalone)
        if standalone:
            extra_args.append("--standalone")
            extra_args.append("--mathjax")
            extra_args.append(f"--metadata=title:{manifest.recipe_name}")

        # Injeção básica de elementos estruturais
        # Para evitar problemas com paths, escrevemos o fragmento de estilo diretamente
        if style.include_header:
            header_html = (
                f"{css_content}"
                f"<div style='display:block; border-bottom: 1px solid #ccc; font-size: 9pt; color: #666; margin-bottom: 20px;'>"
                f"<span>{style.header_text_left}</span>"
                f"<span>{style.header_text_right or manifest.recipe_name}</span>"
                f"</div>"
            )
            with open("engine/src/doc_engine/output_temp_header.html", "w", encoding="utf-8") as f:
                f.write(header_html)
            extra_args.append("--include-before-body=engine/src/doc_engine/output_temp_header.html")

        # 3. Injetamos o rodapé na base (include-after-body) se ativo no manifesto
        if style.include_footer:
            footer_html = (
                f"<div class='doc-footer'>"
                f"<span>{style.footer_text_left}</span>"
                f"<span>Gerado Automaticamente - DocComposer v{manifest.version}</span>"
                f"</div>"
            )
            with open("engine/src/doc_engine/output/temp_footer.html", "w", encoding="utf-8") as f:
                f.write(footer_html)
            extra_args.append("--include-after-body=engine/src/doc_engine/output/temp_footer.html")
        
        pypandoc.convert_file(
            source_file=source_markdown_path,
            to="html5",
            outputfile=output_path,
            extra_args=extra_args
        )

        # Limpeza de resíduos temporários de build
        for temp_file in ["engine/src/doc_engine/output/temp_header.html", "engine/src/doc_engine/output/temp_footer.html"]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        return output_path
