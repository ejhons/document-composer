import os
import pandas as pd
from dcp_engine.compilation.adapters.base import adapter_logger
from dcp_engine.compilation.adapters.base import BaseContentAdapter
from dcp_engine.planning.graph.assets import AssetBundle, ComponentContent
from dcp_engine.runtime.workspace import Workspace
from dcp_engine.planning.graph.component_node import ComponentNode


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
    