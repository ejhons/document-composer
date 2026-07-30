import os
import shutil
from pathlib import Path
from engine.compilation.adapters.base import AssetResult, adapter_logger
from engine.compilation.adapters.base import BaseContentAdapter
from engine.compilation.adapters.assets import Asset, AssetBundle, ComponentContent
from engine.runtime.workspace import Workspace
from engine.frontend.parser import MarkdownParser
from engine.planning.graph.component_node import ComponentNode
from engine.solving.solving_context import SolvingContext

    
class ImageMarkdownAdapter(BaseContentAdapter):
    def __init__(
        self,
        renderer: ImageRenderer | None = None,
        parser: MarkdownParser | None = None
    ):
        self.parser = parser or MarkdownParser()
        self.renderer = renderer or ImageRenderer()

    def convert(
        self,
        node: ComponentNode,
        # context: PlanningContext,
        workspace: Workspace,
        # source_path: str,
        # output_dir: str,
        **kwargs
    ) -> ComponentContent:
        source_path = Path(node.component.source)
        result = self.renderer.render(
            source_path=source_path,
            output_dir=workspace.images_dir #output_dir
        )

        asset = Asset(
            id=result.source.stem,
            type="image",
            source=result.source, #source_path,
            output=result.output #Path(result['output'])#Path(output_dir) / Path(source_path).name,
        )
        parsed = f"![]({asset.output.as_posix()})"#result['output']})"
        # parsed = self.parser.parse(
        #     f"![]({asset.id})"
        # )

        return ComponentContent(
            markdown=parsed,
            assets=AssetBundle(
                assets=[asset]
            ),
        )


class ImageRenderer:
    def render(
        self,
        source_path: Path,
        output_dir: Path          
    ) -> AssetResult:
        """
        Satisfies the Input Port contract. Wraps a raw physical image file 
        into a valid standalone Markdown image token.
        """
        if not source_path.exists():#os.path.exists(source_path):
            adapter_logger.warning(f"Raw image asset missing at: {source_path.as_posix()}")
            raise FileNotFoundError(f"Image missing: {source_path.as_posix()}")
            # return f"\n\n<!-- [Warning] Image missing: {source_path.as_posix()} -->\n\n"
            
        filename = os.path.basename(source_path)
        base_name = os.path.splitext(filename)[0] # Nome do arquivo sem extensão

        target_image_path = output_dir.joinpath(filename) #os.path.join(output_dir, filename)
        os.makedirs(target_image_path, exist_ok=True)
        shutil.copy(source_path, target_image_path)        

        # Retorna a string Markdown que o compilador final precisa para embutir a imagem
        return AssetResult(
            tag= f'Asset - {base_name}',
            source= source_path,
            output= target_image_path
        )

  

# class ImageMarkdownAdapter(BaseContentAdapter):
#     def convert(self, source_path: str, output_resource_dir: str, **kwargs) -> str:
#         """
#         Satisfies the Input Port contract. Wraps a raw physical image file 
#         into a valid standalone Markdown image token.
#         """
#         if not os.path.exists(source_path):
#             adapter_logger.warning(f"Raw image asset missing at: {source_path}")
#             return f"\n\n<!-- [Warning] Image missing: {source_path} -->\n\n"
            
#         base_name = os.path.splitext(os.path.basename(source_path))[0]
#         # Retorna a string Markdown que o compilador final precisa para embutir a imagem
#         return f"\n\n![Asset - {base_name}]({source_path})\n\n"
    