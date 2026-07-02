import os
import pypdfium2 as pdfium
from engine.src.doc_engine.compilation.adapters.adapters import BaseContentAdapter

class PdfToImageMarkdownAdapter(BaseContentAdapter):
    def convert(self, source_path: str, output_dir: str) -> str:
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"PDF asset missing: {source_path}")
        
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        
        print(f"[Adapter - Native] Opening PDF document via embedded Pdfium: {base_name}")
        
        # Abre o documento PDF de forma 100% nativa em Python
        pdf = pdfium.PdfDocument(source_path)
        image_tags = []
        
        # Percorre as páginas usando o índice
        for idx in range(len(pdf)):
            page = pdf[idx]
            
            # Renderiza a página direto para um objeto de Imagem do Pillow (PIL)
            # scale=2 equivale a aproximadamente 144 DPI, excelente qualidade para Word
            pil_image = page.render(scale=2).to_pil()
            
            # Define os caminhos de saída das imagens locais
            image_name = f"{base_name}_page_{idx + 1}.png"
            target_image_path = os.path.join(output_dir, image_name)
            
            # Salva o arquivo em disco
            pil_image.save(target_image_path, "PNG")
            
            # Formata as tags de injeção visual para o compilador Pandoc
            image_tags.append(f"![{base_name} - Page {idx + 1}]({target_image_path})\n\n---\n")
            
        return "\n\n" + "\n".join(image_tags) + "\n"
