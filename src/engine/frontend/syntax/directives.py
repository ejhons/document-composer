from pydantic import BaseModel, Field

class DirectiveCall(BaseModel):
    index: int
    name: str
    raw: str
    # line: int
    # column: int
    start: TextSpan
    end: TextSpan
    arguments: list[DirectiveArgument] = Field(default_factory=list)

class TextSpan(BaseModel):
    line: int
    column: int
    index: int

class DirectiveArgument(BaseModel):
    name: str | None
    expression: Expression
    is_dynamic: bool = False

class Expression(BaseModel):
    source: str
