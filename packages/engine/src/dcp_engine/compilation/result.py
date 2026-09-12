from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class CompilationResult:
    '''
    Result of comilation proccess.
    '''
    format_text: str
    output_compiled: Path
