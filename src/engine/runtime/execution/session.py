from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel

from engine.common.models.workspace import Workspace
from engine.planner.graph.graph import RecipeGraph
from engine.planner.planning_context import PlanningContext
from engine.runtime.execution.context import ExecutionContext
from engine.common.models.recipe import RecipeManifest


class ExecutionSession(BaseModel):
    manifest:RecipeManifest
    execution_context: ExecutionContext
    
    trace: Optional[Any] = None
    graph:Optional[RecipeGraph] = None
    workspace: Optional[Workspace] = None
    