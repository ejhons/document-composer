# from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel, Field

from dcp_engine.language.manifests.loader import ManifestLoader
from dcp_engine.runtime.workspace import Workspace
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.runtime.execution.context import ExecutionContext
from dcp_engine.language.manifests.recipe import RecipeManifest
from dcp_engine.language.syntax.markdown.atomized_markdown import AtomizedMarkdown


class ExecutionSession(BaseModel):
    workspace: Workspace
    
    context: ExecutionContext = Field( 
        default_factory=ExecutionContext
    )
    
    manifest:Optional[RecipeManifest] = None
    trace: Optional[Any] = None
    
    graph:Optional[RecipeGraph] = None
    fragmented_markdown: Optional[AtomizedMarkdown] = None

    def update_context(self):
        if self.graph is not None:
            self.graph.parents    
    # @property
    # def context(self):
    #     return self.context
