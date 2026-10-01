from typing import Dict
from dcp_engine.compilation.compilers.base import BaseCompiler


class CompilerRegistry:
    """Manages routing registry for target distribution format exporters."""
    def __init__(self):
        self._registry: Dict[str, BaseCompiler] = {}

    def register(
            self,
            target_format: str,
            compiler: BaseCompiler
        ):
        self._registry[target_format.lower()] = compiler

    def get(
            self,
            target_format: str
        ) -> BaseCompiler:
        compiler = self._registry.get(target_format.lower())
        if not compiler:
            raise ValueError(f"No output compiler adapter registered for format type: '{target_format}'")
        return compiler
    

