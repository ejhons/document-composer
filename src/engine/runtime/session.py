from pathlib import Path
from typing import Any
from pydantic import BaseModel

from engine.planner.graph.graph import RecipeGraph
from engine.runtime.context import ExecutionContext
from engine.common.models.recipe import RecipeManifest


class ExecutionSession(BaseModel):
    working_directory: Path
    manifest:RecipeManifest
    planning_graph: RecipeGraph
    graph:RecipeGraph
    context: ExecutionContext
    trace: Any