import os
from pathlib import Path
from docx import Document
from engine.compilation.adapters.base import BaseContentAdapter
from engine.compilation.adapters.assets import Asset, AssetBundle, ComponentContent
from engine.runtime.workspace import Workspace
from engine.frontend.parser import MarkdownParser
from engine.planning.graph.component_node import ComponentNode
# from engine.planner.planning_context import PlanningContext


class DocxAdapter(BaseContentAdapter):

    def __init__(
        self,
        parser: MarkdownParser | None = None
    ):
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

        source_path = Path(node.component.source)
        asset = Asset(
            id=source_path.stem,
            type="docx",
            source=source_path,
            output=workspace.documents_dir.joinpath(source_path)# output_dir) / Path(source_path).name,
        )

        placeholder = f'@include("{asset.id}")'

        # parsed = self.parser.parse(placeholder)

        return ComponentContent(
            markdown=placeholder, #parsed,
            assets=AssetBundle(
                assets=[asset]
            ),
        )

class DocxPostCompileAdapter(BaseContentAdapter):
    def convert(
        self,
        node: ComponentNode,
        # context: PlanningContext,
        workspace: Workspace,
        **kwargs
        # source_path: str,
        # output_dir: str
    ) -> ComponentContent:
        # Returns a standard placement string token to be matched post-compilation
        return ComponentContent(
            markdown= f"\n<!-- WORD_MERGE_POINT: {node.component.source} -->\n"
        )

    def execute_binary_merge(
        self,
        master_docx_path: str,
        external_docx_path: str
    ):
        """Specialized secondary action for docx post-processing layer."""
        if not os.path.exists(master_docx_path) or not os.path.exists(external_docx_path):
            raise FileNotFoundError("Missing target binaries for structural append.")
        
        master_doc = Document(master_docx_path)
        external_doc = Document(external_docx_path)
        master_doc.add_page_break()
        
        for element in external_doc.element.body:
            master_doc.element.body.append(element)
            
        master_doc.save(master_docx_path)

        # Asset(
        #     id='',
        #     type='docx',
        #     source=None,
        #     output=None
        # )
