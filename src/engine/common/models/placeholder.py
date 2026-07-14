from pydantic import BaseModel

from engine.planner.graph.component_node import ComponentNode


class Placeholder(BaseModel):
    type:str
    asset_id:ComponentNode

    
class NodePlaceholder(BaseModel):
    node_id:str
    
    @property
    def placeholder(self):
        return f'__dc:node:{self.node_id}__'
    
class PlaceholderEncoder(BaseModel):
    def encode(
        self,
        placeholder:NodePlaceholder
    ):
        return placeholder.placeholder
    
    def decode(
        self,
        coded_placeholder: str
    ):
        return NodePlaceholder(
            node_id='str'
        )