from typing import Any


class InputDefinition:
    name: str
    type: str
    declared: bool
    label: str | None
    description: str | None
    default: Any