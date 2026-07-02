import os
from engine.src.doc_engine.compilation.adapters.adapters import adapter_logger
from engine.src.doc_engine.compilation.adapters.adapters import BaseContentAdapter


class ImageMarkdownAdapter(BaseContentAdapter):
    def convert(self, source_path: str, output_resource_dir: str, **kwargs) -> str:
        """
        Satisfies the Input Port contract. Wraps a raw physical image file 
        into a valid standalone Markdown image token.
        """
        if not os.path.exists(source_path):
            adapter_logger.warning(f"Raw image asset missing at: {source_path}")
            return f"\n\n<!-- [Warning] Image missing: {source_path} -->\n\n"
            
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        # Retorna a string Markdown que o compilador final precisa para embutir a imagem
        return f"\n\n![Asset - {base_name}]({source_path})\n\n"