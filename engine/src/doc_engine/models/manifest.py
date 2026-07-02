from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional

class AssembledManifest(BaseModel):
    document_name: str
    generation_timestamp: str
    engine_version: str
    target_format: str
    injected_parameters: Dict[str, Any]
    compiled_markdown_source: str  # Caminho para o arquivo .md unificado
    generated_resources: List[str] # Lista de imagens/diagramas gerados no processo
