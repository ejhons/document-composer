from typing import Any, Literal

from pydantic import BaseModel, Field


class CompileRequest(BaseModel):
    target_format: Literal[
        "default",
        "md",
        "pdf",
        "docx",
        "html",
    ] = "default"

    # variables: dict[str, Any] = Field(
    #     default_factory=dict
    # )

class CompilationResponse(BaseModel):
    project_id: str
    target_format: str
    artifact: str