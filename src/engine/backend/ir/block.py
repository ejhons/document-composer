from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from engine.common.models.assets import AssetBundle
from engine.common.models.compiled_markdown import CompiledMarkdown
from engine.common.utils.generator import IdGenerator
from engine.frontend.syntax.parsed_markdown import ParsedMarkdown


class IRBlock(BaseModel):
    _id: str = PrivateAttr(default_factory=lambda : IdGenerator.generate('ir'))
    content: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    _parent: Optional[IRBlock]  = PrivateAttr(default=None)
    _children: list[IRBlock] = PrivateAttr(default_factory=list)
    
    model_config = ConfigDict(frozen=True)

    @property
    def id(self):
        return self._id
    
    @property
    def parent(self):
        return self._parent
    
    @property
    def children(self):
        return self._children
    
    @property
    def is_leaf(self) -> bool:
        return len(self._children) == 0

    @property
    def has_children(self) -> bool:
        return len(self._children) > 0

    @property
    def level(self) -> int:
        level = 0
        parent = self._parent

        while parent is not None:
            level += 1
            parent = parent._parent

        return level
    
    @property
    def ancestors(self) -> list["IRBlock"]:
        nodes = []

        parent = self._parent

        while parent is not None:
            nodes.append(parent)
            parent = parent._parent

        return nodes
    
    def walk(self):
        yield self

        for child in self._children:
            yield from child.walk()

    def clone(self) -> "IRBlock":
        return self.model_copy(deep=True)
    
class ComponentIRBlock(IRBlock):
    node_id: Optional[str]
    type: str
    markdown: Optional[ParsedMarkdown] = None
    assets: AssetBundle = Field(default_factory=AssetBundle) # type: ignore