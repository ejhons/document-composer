from pathlib import Path

from pydantic import BaseModel, Field, model_validator
from typing import Any, List, Literal, Optional

from dcp_engine.common.generator import IdGenerator

class DependencyReference(BaseModel):
    expression: str
    directive: str
    dynamic: bool
    line: int | None = None

class RecipeManifest(BaseModel):
    '''
    Grafo estrtural declarado no arquivo de manifesto.
    Gera, praticamente, uma árvore.
    '''
    recipe_name: str
    version: str
    style: StyleConfig
    components: List[ComponentConfig] = Field(default_factory=list)
    inputs: dict[str, Any] = Field(default_factory=dict)
    # Adicionamos o formato de saída padrão do documento (docx ou pdf)
    target_format: Literal["docx", "pdf", "html"] = Field(default="docx")


class ComponentConfig(BaseModel):
    # id: str# = Field(default_factory = IdGenerator.generate)
    type: Literal["template", "external", "generated"]
    source: str
    file_format: Optional[Literal["md", "docx", "pdf", "xlsx", "image", "html"]] = None
    is_required: bool = True
    # Exemplo: "project_type == 'Industrial'" ou "has_elevator == 'Sim'"
    condition: Optional[str] = Field(default=None)
    context: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def solvable(self):
        return (
            self.type == 'template'
            or
            self.file_format == 'md'
        )

    @model_validator(mode="after")
    def infer_file_format(self):
        if self.file_format is not None:
            return self

        extension = Path(self.source).suffix.lower().lstrip(".")

        image_extensions = {
            "png",
            "jpg",
            "jpeg",
            "gif",
            "bmp",
            "tif",
            "tiff",
            "svg",
            "webp",
            "ico",
            "avif",
        }

        mapping = {
            "md": "md",
            "docx": "docx",
            "pdf": "pdf",
            "xlsx": "xlsx",
            "html": "html",
            "htm": "html",
        }

        if extension in image_extensions:
            self.file_format = "image"

        elif extension in mapping:
            self.file_format = mapping[extension]
            
        else:
            raise ValueError(
                f"Não foi possível inferir o file_format a partir da extensão '{extension}'. "
                "Informe file_format explicitamente."
            )

        return self

class StyleConfig(BaseModel):
    reference_docx: Optional[str] = None
    include_header: bool = True
    include_footer: bool = True
    # Novos metadados para estilização dinâmica
    header_text_left: Optional[str] = Field(default="Memorial Descritivo Técnico")
    header_text_right: Optional[str] = Field(default="")
    footer_text_left: Optional[str] = Field(default="Confidencial")
    primary_color: Optional[str] = Field(default="#003366") # Azul Engenharia padrão

