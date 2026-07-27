import re
import base64
import logging
import requests

from typing import Any
from pathlib import Path
from engine.frontend.parser import MarkdownParser
from engine.common.models.workspace import Workspace
from engine.common.exceptions import DownloadException
from engine.backend.adapters.base import BaseContentAdapter
from engine.planner.planning_context import PlanningContext
from engine.planner.graph.component_node import ComponentNode
from engine.common.models.assets import Asset, AssetBundle, ComponentContent

logger = logging.getLogger("doc_engine.adapters")

class MarkdownAdapter(BaseContentAdapter):
    """
    Handles rendering of Markdown components, compiling Jinja variables, 
    and resolving embedded dynamic sub-blocks like inline Mermaid diagrams.
    """
    def __init__(
            self,
            parser: MarkdownParser,
            cache_manager: Any,
            mermaid_adapter: MermaidMarkdownAdapter | None = None
            ):
        self.parser = parser
        self.cache = cache_manager
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
        cache_manager: Any
    ):
        self.parser = parser
        self.cache = cache_manager

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
                diagram_code=block, 
                output_dir=workspace.images_dir
            )
            # Parte para próxima iteração caso não seja criada uma imagem
            if asset is None:
                continue
            # Adiciona os assets gerados ao bundle
            assets.add(asset)
            processed = processed.replace(
                block.full_text,
                f'![Diagram]({asset.output.as_posix()})'
            )

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
        matches = re.findall(
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
        
        asset = Asset(
            id = diagram_id,
            type = 'image',
            source= output_image_path,#source or output_image_path,
            output= output_image_path,
        )

        # Verificação de cache nativa
        if self.cache.is_cached(diagram_id, diagram_hash, [output_image_path]):
            logger.info(f"Cache hit for inline diagram '{diagram_id}'. Reusing PNG asset.")
        else:
            logger.info(f"Cache miss for inline diagram '{diagram_id}'. Fetching cloud render...")
            try:
                graph_bytes = diagram_code.encode('utf-8')
                base64_bytes = base64.b64encode(graph_bytes)
                base64_string = base64_bytes.decode('utf-8')
                
                url = f"[https://mermaid.ink/img/](https://mermaid.ink/img/){base64_string}"
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    with open(output_image_path, 'wb') as f:
                        f.write(response.content)
                    self.cache.update_cache(diagram_id, diagram_hash, [output_image_path])
                else:
                    raise DownloadException("Couldn't using mermaid.ink API")
            except Exception as e:
                logger.error(f"Failed to render inline mermaid block: {e}")
                return None
                    
        return asset


# class DirectiveMarkdownAdapter:
#     def __init__(
#         self,
#         parser: MarkdownParser
#     ):
#         self.parser = parser

#     def convert(
#         self, 
#         source_path: str,
#         output_dir: str,
#         **kwargs
#     ) -> str:     

#         markdown = kwargs.get("raw_markdown")
#         if markdown is None:
#             markdown = self.parser.read_markdown(source_path)

#         node: ComponentNode = kwargs.get('node')
#         # node.inspection.directives
        
#         parsed = self.parser.parse(markdown)

#         for directive in node.inspection.directives:
#             index = directive.index
#             parsed_directive = parsed.find_directive_by_id(index)

#             markdown = markdown.replace(
#                 parsed_directive.raw,
#                 node.resolution.content,
#                 1
#             )
            

#         processed = markdown

#         return processed


# class DirectivePostProcessor:
#     def process(
#         self,
#         node: ComponentNode,
#         content: ComponentContent,
#     ) -> ComponentContent:


#         markdown.replace(
#             directive.span,
#             placeholder,
#         )

#         markdown = content.markdown
#         processed = markdown

#         for directive in node.inspection.directives:
#             handler = directive.name
#             raw = directive.raw

#             if handler is None:
#                 continue

#             placeholder = Placeholder(
#                 type="docx",
#                 asset_id=directive.arguments[0],
#             )
#             handler.process(
#                 markdown,
#                 directive,
#                 content.assets,
#             )

#         return content


    # def _convert_inline_mermaid(self, raw_markdown: str, output_resource_dir: str) -> str:
    #     """Scans rendered text for inline mermaid code blocks and translates them into static images."""
    #     mermaid_pattern = r'```mermaid\s*\n(.*?)\n```'
    #     matches = re.findall(mermaid_pattern, raw_markdown, re.DOTALL)
    #     if not matches:
    #         return raw_markdown

    #     processed_markdown = raw_markdown
    #     os.makedirs(output_resource_dir, exist_ok=True)

    #     for _, diagram_code in enumerate(matches):
    #         # Cria uma assinatura única baseada no próprio código do diagrama
    #         diagram_hash = self.cache.calculate_text_hash(diagram_code)
    #         diagram_id = f"inline_diagram_{diagram_hash[:10]}"
            
    #         image_filename = f"rendered_{diagram_id}.png"
    #         output_image_path = os.path.join(output_resource_dir, image_filename)
            
    #         # Verificação de cache nativa
    #         if self.cache.is_cached(diagram_id, diagram_hash, [output_image_path]):
    #             logger.info(f"Cache hit for inline diagram '{diagram_id}'. Reusing PNG asset.")
    #             image_markdown_tag = f"\n\n![System Diagram]({output_image_path})\n\n"
    #         else:
    #             logger.info(f"Cache miss for inline diagram '{diagram_id}'. Fetching cloud render...")
    #             try:
    #                 graph_bytes = diagram_code.encode('utf-8')
    #                 base64_bytes = base64.b64encode(graph_bytes)
    #                 base64_string = base64_bytes.decode('utf-8')
                    
    #                 url = f"[https://mermaid.ink/img/](https://mermaid.ink/img/){base64_string}"
    #                 response = requests.get(url, timeout=15)
                    
    #                 if response.status_code == 200:
    #                     with open(output_image_path, 'wb') as f:
    #                         f.write(response.content)
    #                     image_markdown_tag = f"\n\n![System Diagram]({output_image_path})\n\n"
    #                     self.cache.update_cache(diagram_id, diagram_hash, [output_image_path])
    #                 else:
    #                     image_markdown_tag = f"\n\n```mermaid\n{diagram_code}\n```\n\n"
    #             except Exception as e:
    #                 logger.error(f"Failed to render inline mermaid block: {e}")
    #                 image_markdown_tag = f"\n\n```mermaid\n{diagram_code}\n```\n\n"
            
    #         full_block_to_replace = f"```mermaid\n{diagram_code}\n```"
    #         processed_markdown = processed_markdown.replace(full_block_to_replace, image_markdown_tag)
            
    #     return processed_markdown

# class MarkdownFieldTemplateAdapter(BaseContentAdapter):
#     # def __init__(self, jinja_env: Any):
#     #     self.jinja_env = jinja_env

#     def convert(self, source_path: str, output_dir: str, **kwargs) -> str:
#         raw_markdown = kwargs.get('raw_markdown')
#         user_inputs: Dict[str, Any] = kwargs.get('user_inputs')
#         output_dir = kwargs.get('raw_markdown', output_dir)

#         if user_inputs is None:
#             raise FileNotFoundError(f"'user_inputs' must be given.")

#         if (raw_markdown is None) and (not os.path.exists(source_path)):
#             raise FileNotFoundError(f"External Markdown file missing: {source_path}")
        
#         if raw_markdown is None:
#             with open(source_path, 'r', encoding='utf-8') as file:
#                 raw_markdown = f"\n\n{file.read()}\n\n"
        
#         return self._render_a_render(raw_markdown, user_inputs, output_dir)

        
#     def _render_a_render(
#             self, 
#             raw_markdown: 
#             str, user_inputs: Dict[str, Any], 
#             output_resource_dir: str
#         ) -> str:
#         """Loads the markdown file, injects context data, and cleans inner syntax blocks."""
#         # 1. Faz o parse do Front Matter e lê o corpo do arquivo
#         parser = MarkdownParser()
#         _, body = parser.parse_front_matter_from_content(raw_markdown)
        
#         # 2. Injeta as variáveis do usuário via Jinja
#         jinja_template = self.jinja_env.from_string(body)
#         rendered_text = jinja_template.render(user_inputs)
        
#         # 3. INTERCEPTAÇÃO INLINE: Limpa o texto traduzindo os blocos dinâmicos embutidos
#         # Se no futuro você quiser interceptar equações complexas ou shorts codes, a regra entra aqui!
#         # final_processed_text = self.convert_inline_mermaid(rendered_text, output_resource_dir)
        
#         return rendered_text
    
# Adicione/Atualize em core/adapters.py
# import os
# import base64
# import requests
# import logging
# from typing import Any

# logger = logging.getLogger("doc_engine.adapters")

# class MermaidMarkdownAdapter: # Herda de BaseAdapter se houver
#     def __init__(self, cache_manager: Any):
#         self.cache = cache_manager

#     def convert(self, source_path: str, output_resource_dir: str) -> str:
#         """
#         Satisfies the Input Port contract. Reads a standalone .mermaid definition file,
#         evaluates global caching hashes, draws the visual layout, and returns the MD image asset string.
#         """
#         if not os.path.exists(source_path):
#             logger.warning(f"Mermaid file source missing at: {source_path}")
#             return ""

#         # Lemos o código-fonte puro do diagrama a partir do arquivo .mermaid indicado no manifesto
#         with open(source_path, "r", encoding="utf-8") as f:
#             diagram_code = f.read().strip()

#         if not diagram_code:
#             return ""

#         # Geramos IDs baseados no nome do arquivo original para evitar colisões
#         base_name = os.path.splitext(os.path.basename(source_path))[0]
#         image_filename = f"rendered_{base_name}.png"
#         output_image_path = os.path.join(output_resource_dir, image_filename)
        
#         # 1. Validação de Cache
#         diagram_hash = self.cache.calculate_text_hash(diagram_code)
#         if self.cache.is_cached(base_name, diagram_hash, [output_image_path]):
#             logger.info(f"Cache hit for diagram component '{base_name}'. Reusing active PNG asset.")
#             return f"\n\n![Diagram - {base_name}]({output_image_path})\n\n"
        
#         # 2. Cache Miss: Requisição à API Externa
#         logger.info(f"Cache miss for diagram '{base_name}'. Rendering dynamic structural layout...")
#         try:
#             graph_bytes = diagram_code.encode('utf-8')
#             base64_bytes = base64.b64encode(graph_bytes)
#             base64_string = base64_bytes.decode('utf-8')
            
#             url = f"https://mermaid.ink/img/{base64_string}"
#             response = requests.get(url, timeout=15)
            
#             if response.status_code == 200:
#                 os.makedirs(output_resource_dir, exist_ok=True)
#                 with open(output_image_path, 'wb') as img_file:
#                     img_file.write(response.content)
                
#                 # Salvando o estado no cache gerenciado
#                 self.cache.update_cache(base_name, diagram_hash, [output_image_path])
#                 return f"\n\n![Diagram - {base_name}]({output_image_path})\n\n"
#             else:
#                 logger.error(f"Mermaid Cloud API returned error code {response.status_code}.")
#                 return f"\n\n```mermaid\n{diagram_code}\n```\n\n"
                
#         except Exception as network_error:
#             logger.error(f"Network transport connection error failed to map diagram: {network_error}")
#             return f"\n\n```mermaid\n{diagram_code}\n```\n\n"
        

#------------------
# class MermaidMarkdownAdapter(BaseContentAdapter):
#     def __init__(self, cache_manager: Any):
#         # Injetamos o gerenciador de cache para que o adaptador decida autonomamente se precisa renderizar
#         self.cache = cache_manager

#     def convert(self, source_path: str, output_dir: str) -> str:
#         if not os.path.exists(source_path):
#             raise FileNotFoundError(f"External Markdown file missing: {source_path}")
#         with open(source_path, 'r', encoding='utf-8') as file:
#             return f"\n\n{file.read()}\n\n"
        

# class MarkdownPassthroughAdapter:
#     """
#     Component Adapter responsible for intercepting raw Mermaid cryptographic text blocks,
#     caching states, fetching vector renders from external APIs, and replacing them with local static images.
#     """
#     def __init__(self, cache_manager: Any):
#         # Injetamos o gerenciador de cache para que o adaptador decida autonomamente se precisa renderizar
#         self.cache = cache_manager

#     def process(self, raw_markdown: str, output_resource_dir: str) -> str:
#         """Scans text for mermaid definitions, handles caching layers and returns valid markdown."""
#         mermaid_pattern = r'```mermaid\s*\n(.*?)\n```'
#         matches = re.findall(mermaid_pattern, raw_markdown, re.DOTALL)
#         if not matches:
#             return raw_markdown

#         processed_markdown = raw_markdown
#         os.makedirs(output_resource_dir, exist_ok=True)

#         for index, diagram_code in enumerate(matches):
#             diagram_id = f"mermaid_diagram_{index + 1}"
#             # Define a unique name and path for each diagram image asset
#             image_filename = f"rendered_diagram_{index + 1}.png"
#             output_image_path = os.path.join(output_resource_dir, image_filename)
            
#             # 1. Calcula hash do texto do diagrama para o cache
#             diagram_hash = self.cache.calculate_text_hash(diagram_code)
#             # 2. Avaliação de Hit no Cache
#             if self.cache.is_cached(diagram_id, diagram_hash, [output_image_path]):
#                 adapter_logger.info(f"Cache hit for diagram layout '{diagram_id}'. Reusing local static PNG.")
#                 image_markdown_tag = f"\n\n![System Diagram]({output_image_path})\n\n"
#             else:
#                 # Cache Miss: Realiza o download real da API externa
#                 adapter_logger.info(f"Cache miss for '{diagram_id}'. Fetching dynamic render from Mermaid API...")
#                 try:
#                     import base64
#                     graph_bytes = diagram_code.encode('utf-8')
#                     base64_bytes = base64.b64encode(graph_bytes)
#                     base64_string = base64_bytes.decode('utf-8')

#                     adapter_logger.info("[Adapter] Generating vector graphic via Mermaid API...")                    
#                     url = f"https://mermaid.ink/img/{base64_string}"
#                     response = requests.get(url, timeout=15)
                    
#                     if response.status_code == 200:
#                         with open(output_image_path, 'wb') as f:
#                             f.write(response.content)
#                         image_markdown_tag = f"\n\n![System Diagram]({output_image_path})\n\n"
#                         # Atualiza o cache do sistema com sucesso
#                         self.cache.update_cache(diagram_id, diagram_hash, [output_image_path])
#                     else:
#                         adapter_logger.warning(f"Mermaid API returned status {response.status_code}. Preserving text block.")
#                         image_markdown_tag = f"\n\n```mermaid\n{diagram_code}\n```\n\n"

#                 except Exception as e:
#                     adapter_logger.error(f"Failed to communicate with rendering API for diagram {diagram_id}: {e}")
#                     image_markdown_tag = f"\n\n```mermaid\n{diagram_code}\n```\n\n"
            
#             # Substituição cirúrgica no texto
#             full_block_to_replace = f"```mermaid\n{diagram_code}\n```"
#             processed_markdown = processed_markdown.replace(full_block_to_replace, image_markdown_tag)
            
#         return processed_markdown

