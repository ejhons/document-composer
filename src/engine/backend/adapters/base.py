import logging
from typing import Any
from abc import ABC, abstractmethod


adapter_logger = logging.getLogger("doc_engine.adapters")
# =====================================================================
# 1. THE PORT (Abstract Base Class)
# =====================================================================
class BaseContentAdapter(ABC):
    """
    The Port contract. Every format-specific adapter must implement this interface
    to guarantee interchangeable processing execution.
    """
    @abstractmethod
    def convert(self, source_path: str, output_dir: str, **kwargs) -> Any:
        """Processes the external file and returns data or handles post-processing."""
        pass

# =====================================================================
# 2. INDEPENDENT ADAPTER COMPONENT UNITS
# =====================================================================
# class ExcelToMarkdownAdapter(BaseContentAdapter):
#     def convert(self, source_path: str, output_dir: str) -> str:
#         if not os.path.exists(source_path):
#             raise FileNotFoundError(f"Spreadsheet asset missing: {source_path}")
#         df = pd.read_excel(source_path).dropna(how='all')
#         print(df)
#         return f"\n\n{df.to_markdown(index=False)}\n\n"

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


# class MermaidMarkdownAdapter(BaseContentAdapter):
#     def __init__(self, cache_manager: Any):
#         # Injetamos o gerenciador de cache para que o adaptador decida autonomamente se precisa renderizar
#         self.cache = cache_manager

#     def convert(self, source_path: str, output_dir: str) -> str:
#         if not os.path.exists(source_path):
#             raise FileNotFoundError(f"External Markdown file missing: {source_path}")
#         with open(source_path, 'r', encoding='utf-8') as file:
#             return f"\n\n{file.read()}\n\n"
        

# # class MermaidMarkdownAdapter(BaseContentAdapter):
# #     def convert(self, source_path: str, output_dir: str) -> str:
# #         if not os.path.exists(source_path):
# #             raise FileNotFoundError(f"External Markdown file missing: {source_path}")
# #         with open(source_path, 'r', encoding='utf-8') as file:
# #             return f"\n\n{file.read()}\n\n"

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
#                 logger.info(f"Cache hit for diagram layout '{diagram_id}'. Reusing local static PNG.")
#                 image_markdown_tag = f"\n\n![System Diagram]({output_image_path})\n\n"
#             else:
#                 # Cache Miss: Realiza o download real da API externa
#                 logger.info(f"Cache miss for '{diagram_id}'. Fetching dynamic render from Mermaid API...")
#                 try:
#                     import base64
#                     graph_bytes = diagram_code.encode('utf-8')
#                     base64_bytes = base64.b64encode(graph_bytes)
#                     base64_string = base64_bytes.decode('utf-8')

#                     logger.info("[Adapter] Generating vector graphic via Mermaid API...")                    
#                     url = f"https://mermaid.ink/img/{base64_string}"
#                     response = requests.get(url, timeout=15)
                    
#                     if response.status_code == 200:
#                         with open(output_image_path, 'wb') as f:
#                             f.write(response.content)
#                         image_markdown_tag = f"\n\n![System Diagram]({output_image_path})\n\n"
#                         # Atualiza o cache do sistema com sucesso
#                         self.cache.update_cache(diagram_id, diagram_hash, [output_image_path])
#                     else:
#                         logger.warning(f"Mermaid API returned status {response.status_code}. Preserving text block.")
#                         image_markdown_tag = f"\n\n```mermaid\n{diagram_code}\n```\n\n"

#                 except Exception as e:
#                     logger.error(f"Failed to communicate with rendering API for diagram {diagram_id}: {e}")
#                     image_markdown_tag = f"\n\n```mermaid\n{diagram_code}\n```\n\n"
            
#             # Substituição cirúrgica no texto
#             full_block_to_replace = f"```mermaid\n{diagram_code}\n```"
#             processed_markdown = processed_markdown.replace(full_block_to_replace, image_markdown_tag)
            
#         return processed_markdown

# class DocxPostCompileAdapter(BaseContentAdapter):
#     def convert(self, source_path: str, output_dir: str) -> str:
#         # Returns a standard placement string token to be matched post-compilation
#         return f"\n<!-- WORD_MERGE_POINT: {source_path} -->\n"

#     def execute_binary_merge(self, master_docx_path: str, external_docx_path: str):
#         """Specialized secondary action for docx post-processing layer."""
#         if not os.path.exists(master_docx_path) or not os.path.exists(external_docx_path):
#             raise FileNotFoundError("Missing target binaries for structural append.")
        
#         master_doc = Document(master_docx_path)
#         external_doc = Document(external_docx_path)
#         master_doc.add_page_break()
        
#         for element in external_doc.element.body:
#             master_doc.element.body.append(element)
            
#         master_doc.save(master_docx_path)

# class MermaidMarkdownAdapter(BaseContentAdapter):
#     """
#     Specialist adapter that intercepts Mermaid code blocks, encodes them,
#     and returns a standard Markdown image injection string.
#     """
#     def convert(self, source_path: str, output_dir: str) -> str:
#         # Esse método cumpre o contrato da Porta abstrata se necessário, 
#         # mas criaremos uma função específica para processar texto em lote (inline).
#         pass

#     @staticmethod
#     def process_inline_diagram(mermaid_code: str, output_image_path: str) -> str:
#         """
#         Takes raw Mermaid text, sends it to the Mermaid.ink cloud rendering API,
#         downloads the generated PNG, and returns the Markdown image syntax.
#         """
#         try:
#             print("[Adapter] Generating vector graphic via Mermaid API...")
            
#             # 1. Clean the code text
#             clean_code = mermaid_code.strip()
            
#             # 2. Convert text to standard base64 for URL transmission
#             code_bytes = clean_code.encode('utf-8')
#             base64_bytes = base64.b64encode(code_bytes)
#             base64_string = base64_bytes.decode('utf-8')
            
#             # 3. Request image from official cloud service
#             # api_url = f"[https://mermaid.ink/img/](https://mermaid.ink/img/){base64_string}"
#             api_url = f"https://mermaid.ink/img/{base64_string}"
#             print(api_url)
#             response = requests.get(api_url, timeout=10)
            
#             if response.status_code == 200:
#                 # Save the image disk asset locally so Pandoc can read it offline
#                 os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
#                 with open(output_image_path, 'wb') as img_file:
#                     img_file.write(response.content)
                
#                 # Return standard Markdown image tag pointing to the local file
#                 return f"\n\n![System Diagram]({output_image_path})\n\n"
#             else:
#                 print(f"[Warning] Mermaid API failed (Status: {response.status_code}). Falling back to code block.")
#                 return f"\n```mermaid\n{mermaid_code}\n```\n"
                
#         except Exception as error:
#             print(f"[Warning] Failed to render Mermaid diagram: {error}. Falling back to text.")
#             return f"\n```mermaid\n{mermaid_code}\n```\n"
