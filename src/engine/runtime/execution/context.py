from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from engine.common.models.inspection import Diagnostic
from engine.common.models.recipe import RecipeManifest
from engine.planner.graph.graph import RecipeGraph
from engine.planner.resources.base import ResourceResolver


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