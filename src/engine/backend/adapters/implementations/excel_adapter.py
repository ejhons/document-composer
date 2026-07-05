import os
import pandas as pd
from engine.backend.adapters.base import adapter_logger
from engine.backend.adapters.base import BaseContentAdapter
# =====================================================================
# 2. INDEPENDENT ADAPTER COMPONENT UNITS
# =====================================================================
class ExcelToMarkdownAdapter(BaseContentAdapter):
    def convert(self, source_path: str, output_dir: str) -> str:
        if not os.path.exists(source_path):
            adapter_logger.error(f"Spreadsheet asset missing: {source_path}")
            raise FileNotFoundError(f"Spreadsheet asset missing: {source_path}")
        df = pd.read_excel(source_path).dropna(how='all')
        print(df)
        return f"\n\n{df.to_markdown(index=False)}\n\n"