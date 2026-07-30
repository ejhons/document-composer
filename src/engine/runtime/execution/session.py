# from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel

from engine.runtime.workspace import Workspace
from engine.frontend.syntax.markdown.atomized_markdown import AtomizedMarkdown
from engine.planning.graph.graph import RecipeGraph
# from engine.planner.planning_context import PlanningContext
from engine.runtime.execution.context import ExecutionContext
from engine.frontend.manifests.recipe import RecipeManifest


class ExecutionSession(BaseModel):
    manifest:RecipeManifest
    execution_context: ExecutionContext
    
    trace: Optional[Any] = None
    workspace: Optional[Workspace] = None
    
    graph:Optional[RecipeGraph] = None
    fragmented_markdown: Optional[AtomizedMarkdown] = None
    