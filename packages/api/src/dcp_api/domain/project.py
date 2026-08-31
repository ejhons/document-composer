from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Project:
    """
    Representa um projeto do Document Composer.
    A entidade não conhece detalhes de persistência.
    """
    id: str
    name: str
    path: Path