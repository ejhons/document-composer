from typing import Dict
from engine.backend.compilers.base import BaseCompilerAdapter


class CompilerRegistry:
    """Manages routing registry for target distribution format exporters."""
    def __init__(self):
        self._registry: Dict[str, BaseCompilerAdapter] = {}

    def register_compiler(
            self,
            target_format: str,
            compiler: BaseCompilerAdapter
        ):
        self._registry[target_format.lower()] = compiler

    def get_compiler(
            self,
            target_format: str
        ) -> BaseCompilerAdapter:
        compiler = self._registry.get(target_format.lower())
        if not compiler:
            raise ValueError(f"No output compiler adapter registered for format type: '{target_format}'")
        return compiler
    

