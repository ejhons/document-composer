from pydantic import BaseModel, Field

class TextSpan(BaseModel):
    line: int
    column: int
    index: int

class Expression(BaseModel):
    source: str

class DirectiveArgument(BaseModel):
    name: str | None
    expression: Expression
    is_dynamic: bool = False
    
class DirectiveCall(BaseModel):
    index: int
    name: str
    raw: str
    start: TextSpan
    end: TextSpan
    arguments: list[DirectiveArgument] = Field(default_factory=list)


