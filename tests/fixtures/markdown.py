import pytest


@pytest.fixture
def simple_markdown():

    return """
# Documento
{{ nome }}
@include("anexo.md")
"""

@pytest.fixture
def markdown_with_fields():

    return """
---
fields:
  flow:
    type: number
    label: Vazão
---

Vazão de Fluxo = {{ flow }} m³/s
"""

@pytest.fixture
def markdown_multiple_directives():
    return """
@include("cover.md")
@include(
    "image.png",
    optional=True
)
@include(
    "table.xlsx"
)
"""

@pytest.fixture
def malformed_directive():
    return """
@include(
    texto
"""

@pytest.fixture
def markdown_dynamic_include():
    return """
@include(
    "image_{{indice}}.png"
)
"""

@pytest.fixture
def markdown_builder():
    def _build(
        front_matter: str = "",
        body: str = ""
    ) -> str:
        if front_matter:
            return f"---\n{front_matter}\n---\n\n{body}"

        return body
    return _build

# content = markdown_builder(
#     front_matter="""
# fields:
#   flow:
#     type: number
# """,
#     body="""
# {{ flow }}

# @include("cover.md")
# """
# )