import os
import re
import base64
import requests

from typing import Any
from pathlib import Path
from dcp_engine.common.cache import StaticCacheManager
from dcp_engine.language.parser import MarkdownParser
from dcp_engine.runtime.logging.log import logger
from dcp_engine.runtime.workspace import Workspace
from dcp_engine.common.exceptions import DownloadException
from dcp_engine.compilation.adapters.base import BaseContentAdapter
from dcp_engine.planning.graph.component_node import ComponentNode
from dcp_engine.planning.graph.assets import Asset, AssetBundle, ComponentContent

# logger = logging.getLogger("doc_engine.adapters")

class MarkdownAdapter(BaseContentAdapter):
    """
    Handles rendering of Markdown components, compiling Jinja variables, 
    and resolving embedded dynamic sub-blocks like inline Mermaid diagrams.
    """
    def __init__(
        self,
        parser: MarkdownParser | None = None,
        cache_manager: StaticCacheManager | None = None,
        mermaid_adapter: MermaidMarkdownAdapter | None = None
    ):
        self.parser = parser or MarkdownParser()
        self.cache = cache_manager or StaticCacheManager()
        self.mermaid_adapter = mermaid_adapter or MermaidMarkdownAdapter(cache_manager=self.cache, parser=parser)

    def convert(
        self, 
        node: ComponentNode,
        # context: PlanningContext,
        workspace: Workspace,
        # source_path: str,
        # output_dir: str,
        **kwargs
    ) -> ComponentContent:   
        # markdown = kwargs.get("raw_markdown")
        markdown = node.resolution.content
        # if markdown is None:
        #     with open(source_path, encoding="utf8") as fp:
        #         markdown = fp.read()

        result = self.mermaid_adapter.convert(
            node,
            # context,
            workspace=workspace,
            **kwargs
        )
        parsed = result.markdown

        return ComponentContent(
            markdown=parsed,
            assets=result.assets,
        )

class MermaidMarkdownAdapter(BaseContentAdapter):
    """
    Handles rendering of Markdown components, compiling Jinja variables, 
    and resolving embedded dynamic sub-blocks like inline Mermaid diagrams.
    """
    def __init__(
        self,
        parser: MarkdownParser,
        cache_manager: StaticCacheManager | None = None,
    ):
        self.parser = parser
        self.cache = cache_manager or StaticCacheManager()

    def convert(
        self, 
        node: ComponentNode,
        # context: PlanningContext,
        workspace: Workspace
        # self,
        # source_path: str,
        # output_dir: str,
        # **kwargs
    ) -> ComponentContent:
        
        markdown = node.resolution.content
        # markdown = kwargs.get("raw_markdown")
        # if markdown is None:
        #     markdown = self.parser.read_markdown(source_path)

        assets = AssetBundle()
        processed = markdown

        #Localiza blocos mermaid dentro do Markdown
        matches = self._find_blocks(markdown)
        for block in matches:
            # Cria o asset do da imagem gerada pela renderização.
            asset = self._render(
                diagram_code=block.group(1), 
                output_dir=workspace.images_dir
            )
            # Parte para próxima iteração caso não seja criada uma imagem
            if asset is None:
                continue
            # Adiciona os assets gerados ao bundle
            assets.add(asset)
            processed = processed.replace(
                block.group(0),
                f'![Diagram]({asset.output.as_posix()})'
            )
            # print(processed)
        return ComponentContent(
            markdown=processed,
            assets=assets
        )


    def _find_blocks(
        self,
        raw_markdown: str
    ) -> list[Any]:
        """Scans rendered text for inline mermaid code blocks and translates them into static images."""
        mermaid_pattern = r'```mermaid\s*\n(.*?)\n```'
        matches = re.finditer(#findall(
            mermaid_pattern,
            raw_markdown,
            re.DOTALL
        )
        return matches
        

    def _render(
        self,
        diagram_code: str,
        # source: Path,
        output_dir: Path
    ) -> Asset | None:
        # Cria uma assinatura única baseada no próprio código do diagrama
        diagram_hash = self.cache.calculate_text_hash(diagram_code)
        diagram_id = f"inline_diagram_{diagram_hash[:10]}"
        
        image_filename = f"rendered_{diagram_id}.png"
        output_image_path = output_dir.joinpath(image_filename)
        # output_image = os.path.join(output_dir, image_filename)
        # output_image_path = Path(output_image)
        
        asset = None
        
        # Verificação de cache nativa
        if self.cache.is_cached(diagram_id, diagram_hash):#, [output_image_path]):
            logger.debug(f"Cache hit for inline diagram '{diagram_id}'. Reusing PNG asset.")
        else:
            logger.debug(f"Cache miss for inline diagram '{diagram_id}'. Fetching cloud render...")
            try:
                graph_bytes = diagram_code.encode('utf-8')
                base64_bytes = base64.b64encode(graph_bytes)
                base64_string = base64_bytes.decode('utf-8')
                
                url = f"https://mermaid.ink/img/{base64_string}"
                processed = f"[https://mermaid.ink/img/](https://mermaid.ink/img/{base64_string})"
                
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
                    
                    with open(output_image_path, 'wb') as f:
                        f.write(response.content)
                    self.cache.update_cache(diagram_id, diagram_hash, [output_image_path])
                    logger.info(f"Image Output path: '{output_image_path}'. ")

                    asset = Asset(
                        id = diagram_id,
                        type = 'image',
                        source= output_image_path,#source or output_image_path,
                        output= output_image_path,
                    )
                                    
                else:
                    raise DownloadException("Couldn't using mermaid.ink API")
            except Exception as e:
                logger.error(f"Failed to render inline mermaid block: {e}")
                return None
                    
        return asset
