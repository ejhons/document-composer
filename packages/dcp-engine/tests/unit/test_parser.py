import pytest

from dcp_engine.language.parser import MarkdownParser
from dcp_engine.language.syntax.fields import InputDefinition
from dcp_engine.language.syntax.inputs import InputReference



def test_read(dummy_markdown):
    parser = MarkdownParser()
    content = parser.read_markdown(dummy_markdown)
    assert content is not None
    assert len(content) > 0

def test_parse_markdown(dummy_markdown):
    parser = MarkdownParser()
    parsed_markdown = parser.parse_file(file_path=dummy_markdown)

    assert parsed_markdown is not None
    assert len(parsed_markdown.fields) == 3
    assert len(parsed_markdown.variables) == 2
    assert len(parsed_markdown.directives) == 1


def test_read_markdown_should_raise_when_file_not_exists():
    parser = MarkdownParser()

    with pytest.raises(FileNotFoundError):
        parser.read_markdown("arquivo_inexistente.md")



def test_read_markdown_should_return_file_content(tmp_path):
    content = "# Meu documento\n\nTexto."

    file = tmp_path / "test.md"
    file.write_text(content, encoding="utf-8")

    parser = MarkdownParser()

    result = parser.read_markdown(str(file))

    assert result == content

def test_parse_front_matter():
    content = """---
title: Documento
author: Everton
---

# Título

Conteúdo.
"""
    parser = MarkdownParser()
    metadata, body = parser.parse_front_matter(content)

    assert metadata == {
        "title": "Documento",
        "author": "Everton",
    }

    assert body.startswith("# Título")


def test_parse_without_front_matter():
    content = """# Documento

Texto simples.
"""
    parser = MarkdownParser()

    metadata, body = parser.parse_front_matter(content)

    assert metadata == {}
    assert body == content

def test_parse_empty_front_matter():
    content = """---

---

Conteúdo.
"""
    parser = MarkdownParser()

    metadata, body = parser.parse_front_matter(content)

    assert metadata == {}
    assert body == "Conteúdo.\n"

def test_extract_directives_empty():
    parser = MarkdownParser()

    directives = parser.extract_directives(
        """
# Documento

Texto qualquer.

{{ cliente }}
"""
    )

    assert directives == []


def test_extract_single_directive():
    parser = MarkdownParser()

    directives = parser.extract_directives(
        """
@repeat(items)

Texto
"""
    )

    assert len(directives) == 1

    directive = directives[0]

    assert directive.name == "repeat"


def test_extract_multiple_directives():
    parser = MarkdownParser()

    directives = parser.extract_directives(
        """
@if(cliente)

Texto

@repeat(items)

Fim
"""
    )

    assert len(directives) == 2

    assert directives[0].name == "if"
    assert directives[1].name == "repeat"


def test_merge_declared_field():
    parser = MarkdownParser()

    fields = {
        "cliente": InputDefinition(
            name="cliente",
            type="text",
            declared=True
        )
    }

    merged = parser.merge_fields_and_variables(
        fields,
        {}
    )

    assert "cliente" in merged
    assert merged["cliente"].references == []


def test_merge_implicit_variable():
    parser = MarkdownParser()

    # references = {
    #     "cliente": [
    #         InputReference(
    #             name="cliente",
    #             raw="{{ cliente }}"
    #         )
    #     ]
    # }
    references = [
            InputReference(
                name="cliente",
                raw="{{ cliente }}"
            )
        ]

    merged = parser.merge_fields_and_variables(
        {},
        references
    )

    assert "cliente" in merged

    field = merged["cliente"]

    assert field.name == "cliente"
    assert len(field.references) == 1


def test_merge_declared_field_with_reference():
    parser = MarkdownParser()

    fields = {
        "cliente": InputDefinition(
            name="cliente",
            type="text",
            declared=True,
            description="Nome do cliente"
        )
    }

    # references = {
    #     "cliente": [
    #         InputReference(
    #             name="cliente",
    #             raw="{{ cliente }}"
    #         )
    #     ]
    # }
    references = [
            InputReference(
                name="cliente",
                raw="{{ cliente }}"
            )
        ]

    merged = parser.merge_fields_and_variables(
        fields,
        references
    )

    field = merged["cliente"]

    assert field.description == "Nome do cliente"
    assert len(field.references) == 1


def test_merge_multiple_references():
    parser = MarkdownParser()

    # references = {
    #     "cliente": [
    #         InputReference(
    #             name="cliente",
    #             raw="{{ cliente }}"
    #         ),
    #         InputReference(
    #             name="cliente",
    #             raw="{{ cliente }}"
    #         ),
    #     ]
    # }
    
    references = [
        InputReference(
            name="cliente",
            raw="{{ cliente }}"
        ),
        InputReference(
            name="cliente",
            raw="{{ cliente }}"
        ),
    ]

    merged = parser.merge_fields_and_variables(
        {},
        references
    )

    assert len(merged["cliente"].references) == 2


