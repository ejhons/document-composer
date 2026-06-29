import os
from warnings import deprecated
import pypandoc

from engine.src.doc_engine.core.models import RecipeManifest

@deprecated
class DocumentCompiler:
    def __init__(self, manifest: RecipeManifest):
        self.manifest = manifest

    def compile_to_docx(self, source_markdown_path: str, output_docx_path: str) -> str:
        """
        Compiles a raw Markdown file into a structured, stylized Word Document (.docx)
        using a reference file for consistent headers, footers, and fonts.
        """
        if not os.path.exists(source_markdown_path):
            raise FileNotFoundError(f"Source file not found: {source_markdown_path}")

        # Pandoc compilation arguments
        # --yaml-metadata-block allows parsing title, author blocks elegantly
        # --katex/--mathjax flags tell pandoc to natively map math syntax blocks
        # extra_args = ["--yaml-metadata-block"]
        extra_args = ["--webtex"]

        # Bind the reference style document if provided in the manifest configuration
        reference_path = self.manifest.style.reference_docx
        if reference_path and os.path.exists(reference_path):
            extra_args.append(f"--reference-doc={reference_path}")
        else:
            print(f"[Warning] Reference style document missing or unconfigured. Default layouts applied.")

        print(f"[Compiling] Transforming Markdown structural data into native Docx layout...")
        
        # Trigger the Pandoc core conversion pipeline
        pypandoc.convert_file(
            source_file=source_markdown_path,
            to="docx",
            outputfile=output_docx_path,
            extra_args=extra_args
        )

        return output_docx_path
    
    def compile_to_pdf(self, source_markdown_path: str, output_pdf_path: str) -> str:
        """
        Compiles a raw Markdown file into a professional PDF document.
        Uses Pandoc's PDF engine routing capabilities.
        """
        if not os.path.exists(source_markdown_path):
            raise FileNotFoundError(f"Source file not found: {source_markdown_path}")

        print(f"[Compiling] Transforming Markdown structural data into native PDF layout...")

        # Argumentos para o PDF:
        # --webtex: Processa as equações LaTeX perfeitamente para imagens/vetores no PDF
        # -V geometry: Define margens padrão profissionais (2.5cm) diretamente via comando
        extra_args = [
            "--webtex",
            "-V", "geometry:margin=2.5cm",
            "-V", "lang=pt-BR"
        ]

        # Executa a chamada do Pandoc direcionando para PDF
        # Nota: O Pandoc utiliza por padrão o wkhtmltopdf ou xelatex/pdflatex em background.
        # Caso queira usar um motor HTML leve e nativo, podemos especificar --pdf-engine=weasyprint
        pypandoc.convert_file(
            source_file=source_markdown_path,
            to="pdf",
            outputfile=output_pdf_path,
            extra_args=extra_args
        )

        return output_pdf_path