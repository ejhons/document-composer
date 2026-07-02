
from typing import Any

from pydantic import BaseModel

from engine.src.doc_engine.analysis.syntax.fields import FieldDefinition
from engine.src.doc_engine.analysis.syntax.directives import DirectiveCall
from engine.src.doc_engine.analysis.syntax.variables import VariableReference


class ParsedMarkDown(BaseModel):
    metadata: dict[str, Any]          # sem a chave "fields"
    fields: dict[str, FieldDefinition]
    variables: list[VariableReference]
    directives: list[DirectiveCall]
    body: str
    # metadata:dict[str, Any]
    # body: str
    # fields: dict[str, FieldDefinition]
    # variables: list[VariableReference]
    # directives: list[DirectiveCall]
