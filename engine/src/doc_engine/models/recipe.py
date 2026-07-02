from pydantic import BaseModel, Field
from typing import Any, List, Literal, Optional

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
    components: List[ComponentConfig]
    inputs: dict[str, Any] = Field(default_factory=dict)
    # Adicionamos o formato de saída padrão do documento (docx ou pdf)
    target_format: Literal["docx", "pdf", "html"] = Field(default="docx")

class ComponentConfig(BaseModel):
    id: str
    type: Literal["template", "external", "generated"]
    source: str
    file_format: Optional[Literal["md", "docx", "pdf", "xlsx", "image", "html"]] = None
    is_required: bool = True
    # Exemplo: "project_type == 'Industrial'" ou "has_elevator == 'Sim'"
    condition: Optional[str] = Field(default=None)
    context: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

# Atualize no core/models.py
class StyleConfig(BaseModel):
    reference_docx: Optional[str] = None
    include_header: bool = True
    include_footer: bool = True
    # Novos metadados para estilização dinâmica
    header_text_left: Optional[str] = Field(default="Memorial Descritivo Técnico")
    header_text_right: Optional[str] = Field(default="")
    footer_text_left: Optional[str] = Field(default="Confidencial")
    primary_color: Optional[str] = Field(default="#003366") # Azul Engenharia padrão

