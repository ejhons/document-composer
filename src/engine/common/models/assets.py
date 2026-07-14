from pathlib import Path
from dataclasses import Field
from pydantic import BaseModel
from engine.common.models.compiled_markdown import CompiledMarkdown


class Asset(BaseModel):
    id: str
    type: str
    source: Path
    output: Path
    metadata: dict = Field(default_factory=dict) # type: ignore


class AssetBundle(BaseModel):
    assets:list[Asset] = Field(default_factory=list) # type: ignore

    def add(self, asset: Asset):
        self.assets.append(asset)

    def extend(self, other: "AssetBundle"):
        self.assets.extend(other.assets)

    
class ComponentContent(BaseModel):
    markdown:str
    # markdown: ParsedMarkdown
    assets:AssetBundle = Field(default_factory=AssetBundle)
