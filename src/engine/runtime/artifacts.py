from typing import Any
from pydantic import BaseModel


class OutputArtifact(BaseModel):
    format: str
    content: Any

'''
Markdown
↓
content = "# Memorial..."
Imagem
↓
content = bytes(...)
Tabela
↓
content = DataFrame(...)
Somente no final um WriterAdapter decide
DOCX
PDF
ZIP
API
HTML

Isso desacopla completamente a compilação do destino.
'''