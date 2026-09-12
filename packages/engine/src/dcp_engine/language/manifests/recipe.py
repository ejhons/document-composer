import os
import json
from enum import StrEnum
from pathlib import Path
from typing import Any, List, Literal, Optional
from pydantic import BaseModel, Field, model_validator

from dcp_engine.runtime.logging.log import logger

# logger = logging.getLogger("doc_engine.pipeline")

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
    inputs: dict[str, Any] = Field(default_factory=dict)
    components: List[ComponentConfig] = Field(default_factory=list)
    target_format: Literal["docx", "pdf", "html", "md"] = Field(default="docx")

    @classmethod
    def from_file(
        cls,
        manifest_path: str
    ) -> RecipeManifest:
        
        if not os.path.exists(manifest_path):
            logger.error(f"Assembly recipe manifest not found at: {manifest_path}")
            raise FileNotFoundError(f"Recipe manifest missing: {manifest_path}")
                
        with open(manifest_path, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)

        generated_manifest = cls(**raw_data)

        return generated_manifest
    

class ComponentType(StrEnum):
    INTERNAL = 'internal'
    EXTERNAL = 'external'

class ComponentConfig(BaseModel):
    # id: str# = Field(default_factory = IdGenerator.generate)
    # type: Literal["template", "external", "generated"]
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
            # self.type == 'template'
            # or
            self.file_format == 'md'
        )

    def type(self, component_folder: Path):
        '''
        Identifies if file 
        '''
        # Relative addresses can only correspond to files in workspace
        if not Path(str).is_absolute():
            return ComponentType.INTERNAL
        # If component folder is not given, absolute paths are treated as External
        if component_folder is None:
            return ComponentType.EXTERNAL
        # If component is in component folder it's marked as Internal to Workspace
        if Path(str).is_relative_to(component_folder):
            return ComponentType.INTERNAL
        # Otherwise, file is External.
        return ComponentType.EXTERNAL

    
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

