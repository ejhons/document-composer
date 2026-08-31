from typing import Dict
from dcp_engine.compilation.adapters.base import BaseContentAdapter


# =====================================================================
# 3. THE ADAPTER REGISTRY (The Registry Administrator)
# =====================================================================
class AdapterRegistry:
    """
    Manages the format-to-adapter mapping bindings dynamically.
    Acts as the single point of entry for format resolution.
    """
    def __init__(self):
        self._registry: Dict[str, BaseContentAdapter] = {}

    def get(self, format_extension: str) -> BaseContentAdapter:
        """Retrieves the designated adapter instance or raises clean routing exceptions."""
        adapter = self._registry.get(format_extension.lower())
        if not adapter:
            raise ValueError(f"No adapter registered for format type: '{format_extension}'")
        return adapter
    
    def register(self, format_extension: str, adapter: BaseContentAdapter):
        """Binds a specific file extension format to an adapter class instance."""
        self._registry[format_extension.lower()] = adapter

