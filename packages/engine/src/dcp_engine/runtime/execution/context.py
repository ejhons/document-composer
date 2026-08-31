from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from dcp_engine.solving.inspection.result import Diagnostic



class ExecutionContext(BaseModel):
    inputs: dict[str, Any] = Field(default_factory=dict)
    diagnostics: list[Diagnostic] = Field(default_factory=list)
    # recipe: RecipeManifest
    # graph: RecipeGraph
    # variables: dict[str, Any]
    # outputs: dict[str, Any] #context.outputs[node.id] = artifact
    # resources: ResourceResolver
    # working_directory: Path

    @property
    def pending_inputs(self):
        return set([
            key
            for key,value in self.inputs
            if value is None
        ])