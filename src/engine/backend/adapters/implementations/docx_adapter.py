import os
from docx import Document
from engine.backend.adapters.base import BaseContentAdapter


class DocxPostCompileAdapter(BaseContentAdapter):
    def convert(self, source_path: str, output_dir: str) -> str:
        # Returns a standard placement string token to be matched post-compilation
        return f"\n<!-- WORD_MERGE_POINT: {source_path} -->\n"

    def execute_binary_merge(self, master_docx_path: str, external_docx_path: str):
        """Specialized secondary action for docx post-processing layer."""
        if not os.path.exists(master_docx_path) or not os.path.exists(external_docx_path):
            raise FileNotFoundError("Missing target binaries for structural append.")
        
        master_doc = Document(master_docx_path)
        external_doc = Document(external_docx_path)
        master_doc.add_page_break()
        
        for element in external_doc.element.body:
            master_doc.element.body.append(element)
            
        master_doc.save(master_docx_path)
