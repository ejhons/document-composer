import os
from pathlib import Path
from pydantic import BaseModel
import pypdfium2 as pdfium
from engine.backend.adapters.base import AssetResult, BaseContentAdapter
from engine.common.models.assets import Asset, AssetBundle, ComponentContent
from engine.common.models.workspace import Workspace
from engine.frontend.parser import MarkdownParser
from engine.planner.graph.component_node import ComponentNode
from engine.planner.planning_context import PlanningContext



class PdfToImageMarkdownAdapter(BaseContentAdapter):
    def __init__(
        self,
        renderer: PdfRenderer | None = None,
        parser: MarkdownParser | None = None
    ):
        self.renderer = renderer or PdfRenderer()
        self.parser = parser or MarkdownParser()

    def convert(
        self,
        node: ComponentNode,
        # context: PlanningContext,
        workspace: Workspace,
        # source_path: str,
        # output_dir: str,
        **kwargs
    ) -> ComponentContent:

        markdown = []
        assets = AssetBundle()

        pages = self.renderer.render(
            source_path=Path(node.component.source),
            output_dir=workspace.images_dir,
            # source_path,
            # output_dir
        )

        for page in pages:
            asset = Asset(
                id=page.tag,
                type="image",
                source=page.source,
                output=page.output,
            )

            assets.add(asset)
            markdown.append(f"![]({asset.id})")

        parsed = "\n\n".join(markdown)
        # parsed = self.parser.parse("\n\n".join(markdown))

        return ComponentContent(
            markdown=parsed,
            assets=assets,
        )

class PdfRenderer():
    def render(
        self,
        source_path: Path,
        output_dir: Path
    ) -> list[AssetResult]:#Page]:
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"PDF asset missing: {source_path}")

        # bundle = AssetBundle()
        pages:list[AssetResult] = []
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(source_path))[0]

        # source_path = Path(source_filename)        
        print(f"[Adapter - Native] Opening PDF document via embedded Pdfium: {base_name}")
        
        # Abre o documento PDF de forma 100% nativa em Python
        pdf = pdfium.PdfDocument(source_path)
        # image_tags = []
        
        # Percorre as páginas usando o índice
        for idx in range(len(pdf)):
            page = pdf[idx]
            # Renderiza a página direto para um objeto de Imagem do Pillow (PIL)
            # scale=2 equivale a aproximadamente 144 DPI, excelente qualidade para Word
            pil_image = page.render(scale=2).to_pil()
            # Define os caminhos de saída das imagens locais
            image_name = f"{base_name}_page_{idx + 1}.png"
            target_image_path = output_dir.joinpath(image_name) #os.path.join(output_dir, image_name)
            # Salva o arquivo em disco
            pil_image.save(target_image_path, "PNG")
            # Formata as tags de injeção visual para o compilador Pandoc
            # image_tags.append(f"![{base_name} - Page {idx + 1}]({target_image_path})\n\n---\n")
            pages.append(
                AssetResult(
                    tag=f'{base_name} - Page {idx + 1}',
                    source=source_path,
                    output=target_image_path
                )
            )
            
        return pages#"\n\n" + "\n".join(image_tags) + "\n"
    


# class PdfToImageMarkdownAdapter(BaseContentAdapter):
#     def convert(self, source_path: str, output_dir: str) -> str:
#         if not os.path.exists(source_path):
#             raise FileNotFoundError(f"PDF asset missing: {source_path}")
        
#         os.makedirs(output_dir, exist_ok=True)
#         base_name = os.path.splitext(os.path.basename(source_path))[0]
        
#         print(f"[Adapter - Native] Opening PDF document via embedded Pdfium: {base_name}")
        
#         # Abre o documento PDF de forma 100% nativa em Python
#         pdf = pdfium.PdfDocument(source_path)
#         image_tags = []
        
#         # Percorre as páginas usando o índice
#         for idx in range(len(pdf)):
#             page = pdf[idx]
            
#             # Renderiza a página direto para um objeto de Imagem do Pillow (PIL)
#             # scale=2 equivale a aproximadamente 144 DPI, excelente qualidade para Word
#             pil_image = page.render(scale=2).to_pil()
            
#             # Define os caminhos de saída das imagens locais
#             image_name = f"{base_name}_page_{idx + 1}.png"
#             target_image_path = os.path.join(output_dir, image_name)
            
#             # Salva o arquivo em disco
#             pil_image.save(target_image_path, "PNG")
            
#             # Formata as tags de injeção visual para o compilador Pandoc
#             image_tags.append(f"![{base_name} - Page {idx + 1}]({target_image_path})\n\n---\n")
            
#         return "\n\n" + "\n".join(image_tags) + "\n"
    