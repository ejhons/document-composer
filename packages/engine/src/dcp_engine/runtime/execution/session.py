# from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel

from dcp_engine.runtime.workspace import Workspace
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.runtime.execution.context import ExecutionContext
from dcp_engine.language.manifests.recipe import RecipeManifest
from dcp_engine.language.syntax.markdown.atomized_markdown import AtomizedMarkdown


class ExecutionSession(BaseModel):
    manifest:RecipeManifest
    execution_context: ExecutionContext
    
    trace: Optional[Any] = None
    workspace: Optional[Workspace] = None
    
    graph:Optional[RecipeGraph] = None
    fragmented_markdown: Optional[AtomizedMarkdown] = None
    