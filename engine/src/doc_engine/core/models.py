from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Any

class FieldDefinition(BaseModel):
    data_type: Literal["text", "number", "date", "table"] = Field(default="text")
    label: str
    description: Optional[str] = None

class ComponentConfig(BaseModel):
    id: str
    type: Literal["template", "external"]
    source: str
    # Nova propriedade para sabermos exatamente como tratar o arquivo externo
    file_format: Optional[Literal["md", "docx", "pdf", "xlsx", "image"]] = None
    is_required: bool = True
    # Nova propriedade para Regras Condicionais
    # Exemplo: "project_type == 'Industrial'" ou "has_elevator == 'Sim'"
    condition: Optional[str] = Field(default=None)

# class StyleConfig(BaseModel):
#     reference_docx: Optional[str] = None
#     include_header: bool = True
#     include_footer: bool = True

class RecipeManifest(BaseModel):
    recipe_name: str
    version: str
    style: StyleConfig
    components: List[ComponentConfig]
    # Adicionamos o formato de saída padrão do documento (docx ou pdf)
    target_format: Literal["docx", "pdf", "html"] = Field(default="docx")

class AssembledManifest(BaseModel):
    document_name: str
    generation_timestamp: str
    engine_version: str
    target_format: str
    injected_parameters: Dict[str, Any]
    compiled_markdown_source: str  # Caminho para o arquivo .md unificado
    generated_resources: List[str] # Lista de imagens/diagramas gerados no processo

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