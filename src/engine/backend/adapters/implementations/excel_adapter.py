import os
import pandas as pd
from engine.backend.adapters.base import adapter_logger
from engine.backend.adapters.base import BaseContentAdapter
from engine.common.models.assets import AssetBundle, ComponentContent
from engine.common.models.workspace import Workspace
from engine.planner.graph.component_node import ComponentNode
from engine.planner.planning_context import PlanningContext


class ExcelToMarkdownAdapter(BaseContentAdapter):
    def convert(
        self,
        node: ComponentNode,
        # context: PlanningContext,
        workspace: Workspace
        # source_path: str,
        # output_dir: str
    ) -> ComponentContent:
        source_path = node.component.source
        if not os.path.exists(source_path):
            adapter_logger.error(f"Spreadsheet asset missing: {source_path}")
            raise FileNotFoundError(f"Spreadsheet asset missing: {source_path}")
        df = pd.read_excel(source_path).dropna(how='all')
        
        markdown = df.to_markdown(index=False)
        parsed = f"\n\n{markdown}\n\n"

        return ComponentContent(
            markdown=parsed,
            assets=AssetBundle(),
        )
        # return f"\n\n{df.to_markdown(index=False)}\n\n"
    


# =====================================================================
# 2. INDEPENDENT ADAPTER COMPONENT UNITS
# =====================================================================
# class ExcelToMarkdownAdapter(BaseContentAdapter):
#     def convert(
#         self,
#         source_path: str,
#         output_dir: str
#     ) -> str:
#         if not os.path.exists(source_path):
#             adapter_logger.error(f"Spreadsheet asset missing: {source_path}")
#             raise FileNotFoundError(f"Spreadsheet asset missing: {source_path}")
#         df = pd.read_excel(source_path).dropna(how='all')
        
#         # CompiledMarkdown()

#         # print(df)
#         return f"\n\n{df.to_markdown(index=False)}\n\n"
    